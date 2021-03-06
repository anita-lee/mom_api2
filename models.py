from database import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

DEFAULT_PROFILE_PIC = "https://images.unsplash.com/photo-1621077699196-15b4693707d7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80"

############## STUDENT MODEL ###########################

class Student(db.Model):
    """ Student model """

    __tablename__ = 'students'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    birth_date = db.Column(
        db.String,
        nullable=False
    )

    classroom = db.Column(
        db.String(50),
        nullable=True
    )

    image_url = db.Column(
        db.Text,
    )

    @classmethod
    def get_by_id(cls, id):
        """ Get student by id """

        return cls.query.filter_by(id=id).first()


    @classmethod
    def add(cls, last_name, first_name, birth_date, classroom, image_url):
        """ Add a student. """

        student = Student(
            last_name=last_name,
            first_name=first_name,
            birth_date=birth_date,
            classroom=classroom,
            image_url=image_url or DEFAULT_PROFILE_PIC,
        )

        db.session.add(student)

        return student

    def serialize(self):
        """ Serialize student """

        return {
            'id': self.id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'classroom': self.classroom,
            'image_url': self.image_url
        }

############## EMERGENCY CONTACT MODEL ###########################

class Contact(db.Model):
    """ Contact model """

    __tablename__ = 'contacts'

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
    )

    name = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=True
    )

    phone = db.Column(
        db.String(50),
        nullable=True
    )

    other = db.Column(
        db.String(50),
        nullable=True
    )

    relation = db.Column(
        db.String(50),
        nullable=True
    )

    is_primary = db.Column(
        db.String(50)
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    @classmethod
    def get_by_id(cls, student_id):
        """ Get contacts by id """

        return cls.query.filter_by(student_id=student_id).all()

    def serialize(self):
        """ Serialize contact """

        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'other': self.other,
            'relation': self.relation
        }

############## MEDICAL RECORD MODEL ###########################

class MedicalRecord(db.Model):
    """ Medical record model """

    __tablename__ = 'medical_records'

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id', ondelete='CASCADE'),
        primary_key=True
    )

    student_weight = db.Column(
        db.Float,
        nullable=True
    )

    student_height = db.Column(
        db.Float,
        nullable=True
    )

    polio = db.Column(
        db.String,
        nullable=True
    )

    mmr = db.Column(
        db.String,
        nullable=True
    )

    covid1 = db.Column(
        db.String,
        nullable=True
    )

    covid2 = db.Column(
        db.String,
        nullable=True
    )

    flu = db.Column(
        db.String,
        nullable=True
    )

    tb = db.Column(
        db.String,
        nullable=True
    )

    tetanus = db.Column(
        db.String,
        nullable=True
    )

    @classmethod
    def get_by_id(cls, student_id):
        """ Get medical record by id """

        return cls.query.filter_by(student_id=student_id).first()

    def serialize(self):
        """Serialize medical record"""

        return {
            'student_id': self.student_id,
            'student_weight': self.student_weight,
            'student_height': self.student_height,
            'polio': self.polio,
            'mmr': self.mmr,
            'covid1': self.covid1,
            'covid2': self.covid2,
            'flu': self.flu,
            'tb': self.tb,
            'tetanus': self.tetanus
        }

############## USER MODEL ###########################

class User(db.Model):
    """ User model """

    __tablename__ = 'users'

    username = db.Column(
        db.String(20),
        primary_key=True
    )

    password = db.Column(
        db.String,
        nullable=False
    )

    first_name = db.Column(
        db.String(20),
        nullable=False
    )

    last_name = db.Column(
        db.String(20),
        nullable=False
    )

    email = db.Column(
        db.String(40),
        nullable=False,
        unique=True
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    is_guardian = db.Column(
        db.String(5),
        default=True
    )

    @classmethod
    def signup(cls, username, password, first_name, last_name, email, phone):
        """ Signup user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            is_guardian=True
        )

        db.session.add(user)

        return user

    @classmethod
    def login(cls, username, password):
        """ Login user """

        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user

        return False

    def __repr__(self):
        return f"<User {self.username}: {self.email}>"

    def serialize(self):
        """ Serialize user """

        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'is_guardian': self.is_guardian,
        }

############## GUARDIAN - CHILD RELATIONS MODEL ###########################

class GuardianChild(db.Model):
    """ GuardianChild model """

    __tablename__ = 'guardian_children'

    guardian_username = db.Column(
        db.String(50),
        db.ForeignKey('users.username', ondelete='CASCADE'),
        primary_key=True,
    )

    child_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id', ondelete='CASCADE'),
        primary_key=True,
    )

    child = db.relationship(
        'Student',
        backref=db.backref('guardian_children', lazy=True)
    )

    user = db.relationship(
        'User',
        backref=db.backref('guardian_children', lazy=True)
    )

    def __repr__(self):
        return f"<Guardian {self.guardian_username}: {self.child_id}>"

    @classmethod
    def get_by_guardian(cls, guardian_username):
        """ Get children by guardian """

        return cls.query.filter_by(guardian_username=guardian_username).all()

    def serialize(self):
        """ Serialize guardian child """

        return {
            'guardian_username': self.guardian_username,
            'child_id': self.child_id
        }

def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
