class PatientInformation:
    name = ''
    surname = ''
    age = 0
    sex = ''
    weight = 0
    comment = ''

    def __init__(self, name: str = 'John', surname: str = 'Doe', age: int = 22, sex: str = 'unverified',
                 weight: int = 80, comment: str = 'Headache'):
        self.name = name
        self.surname = surname
        self.age = age
        self.sex = sex
        self.weight = weight
        self.comment = comment
