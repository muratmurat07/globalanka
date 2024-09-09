from django.db import models

from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    StudentClass,
    Subject,
)
from apps.students.models import Student

from .utils import score_grade


# Create your models here.
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name = "Öğrenci")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, verbose_name = "Eğitim Yılı")
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, verbose_name = "Dönem")
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, verbose_name = "Sınıfı")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name = "Ders")
    test_score = models.IntegerField(default=0, verbose_name = "1. Sınav")
    exam_score = models.IntegerField(default=0, verbose_name = "2. Sınav")

    class Meta:
        ordering = ["subject"]

    def __str__(self):
        return f"{self.student} {self.session} {self.term} {self.subject}"

    def total_score(self):
        return (self.test_score + self.exam_score)/2

    def grade(self):
        return score_grade(self.total_score())
