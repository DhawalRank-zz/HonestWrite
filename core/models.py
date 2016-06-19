# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.contrib.postgres.fields import ArrayField
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

    def __str__(self):
        return self.username

    def __int__(self):
        return self.username

    def __unicode__(self):
        return self.username


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FClass(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.ForeignKey(AuthUser, db_column='username', null=True, on_delete=models.CASCADE)
    c_style = models.CharField(max_length=40)
    c_topic = models.CharField(max_length=40)
    c_duedate = models.DateField(max_length=40)

    class Meta:
        managed = False
        db_table = 'fclass'
        unique_together = (('id', 'username'),)

    @property
    def user_name(self):
        try:
            return self.username.username
        except ValueError:
            return self.username.id
    def class_id(self):
        try:
            return self.id
        except ValueError:
            return self.id

    def __int__(self):
        return self.id


class UFaculty(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(AuthUser, db_column='username', null=True)
    f_school = models.CharField(max_length=40)
    f_faculty = models.CharField(max_length=40)
    f_major = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'ufaculty'

    def user_name(self):
        try:
            return self.username.username
        except ValueError:
            return self.username.id

    def __str__(self):
        return self.username.username


class stuClass(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(AuthUser, db_column='username', null=True)
    classid = models.ForeignKey(FClass, db_column='classid', null=True)

    class Meta:
        managed = False
        db_table = 'stuclass'

    def class_name(self):
        try:
            return self.classid.id
        except ValueError:
            return self.classid.id

    def __str__(self):
        return str(self.classid.id)

class CQuestions(models.Model):
    qid = models.AutoField(primary_key=True)
    classid = models.ForeignKey(FClass, null=False, db_column='classid')
    qstring = models.CharField(max_length=200, null=False, blank=False)
    option = ArrayField(models.CharField(max_length=200), blank=False, null=False)
    answers = ArrayField(models.CharField(max_length=200), blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'cquestions'


class CResults(models.Model):
    rid = models.AutoField(primary_key=True)
    classid = models.ForeignKey(FClass, null=False, db_column='classid')
    username = models.ForeignKey(AuthUser, null=False, db_column='username')
    grade = models.CharField(null=False, blank=False, default='TBD', max_length=10)

    class Meta:
        managed = False
        db_table = 'cresults'

    def user_name(self):
        try:
            return self.username.username
        except ValueError:
            return self.username.id

    def __str__(self):
        return self.username.username

class UStudent(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(AuthUser, db_column='username', null=True)
    s_school = models.CharField(max_length=40)
    s_faculty = models.CharField(max_length=40)
    s_major = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'ustudent'

    def user_name(self):
        try:
            return self.username.username
        except ValueError:
            return self.username.id

    def __str__(self):
        return self.username.username
