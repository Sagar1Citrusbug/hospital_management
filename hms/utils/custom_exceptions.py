from dataclasses import dataclass


@dataclass(frozen=True)
class UserRegistrationException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class UserAlreadyExistsException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class UserLoginException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class UserLogoutException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class DoctorCreationException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class DoctorEditException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class DeleteDoctorException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class PatientCreationException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class EditPatientException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class DeletePatientException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class AppointmentCreationException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class EditAppointmentException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class DeleteAppointmentException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"
