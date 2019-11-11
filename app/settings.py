#!/usr/bin/env python
#coding:utf-8

"""
Django settings for wdcmdb project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from config.config import db_config
dbinfo = db_config()

import os
# 添加mysql数据库连接，但是由于python3已经将数据库模块改成了pymysql，不再是MySQLdb
# 但是如果还想要使用以前的MySQLdb连接方式，可以将pymysql别名为MySQLd
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*@o9cx(fbwp(%(=^uo4hti83cpo7i399bf-xyzqsd$f-!f9dky'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'assets.apps.AssetsConfig',
    'accounts',
    'assets',
    'config',
    'deploy',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 添加SessionAuthenticationMiddleware中间件
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': dbinfo['name'],
        'USER': dbinfo['user'],
        'PASSWORD': dbinfo['pw'],
        'HOST': dbinfo['host'],
        'PORT': dbinfo['port'],
        'CHARSET':'utf8',       ##设置字符集，不然会出现中文乱码
        #'OPTIONS': {
        #    'sql_mode': 'traditional',  
        #    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        #    }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

#jason modify: off
#USE_TZ = True    # 如果只是内部使用的系统，这行建议为false，不然会有时区问题


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# 添加静态目录路径
STATICFILES_DIRS = (
    "%s/%s" %(BASE_DIR, "statics"),
)
#print("--->STATICFILES_DIRS: ",STATICFILES_DIRS)
# Django允许你通过修改setting.py文件中的 AUTH_USER_MODEL 设置覆盖默认的User模型，其值引用一个自定义的模型。
AUTH_USER_MODEL = 'accounts.UserProfile'

# token超时时间为120秒
TOKEN_TIMEOUT = 120

# 覆盖原来的登录模块，指定如果未登录，那么则跳到默认的登录页/login/
LOGIN_URL = '/login/'