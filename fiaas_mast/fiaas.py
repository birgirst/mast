#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six
from k8s.base import Model
from k8s.fields import Field, RequiredField, ListField
from k8s.models.common import ObjectMeta


class FiaasApplicationSpec(Model):
    application = RequiredField(six.text_type)
    image = RequiredField(six.text_type)
    config = RequiredField(dict)


class FiaasApplication(Model):
    class Meta:
        url_template = "/apis/fiaas.schibsted.io/v1/namespaces/{namespace}/applications/{name}"
        watch_list_url = "/apis/fiaas.schibsted.io/v1/watch/applications"

    # Workaround for https://github.com/kubernetes/kubernetes/issues/44182
    apiVersion = Field(six.text_type, "fiaas.schibsted.io/v1")
    kind = Field(six.text_type, "Application")

    metadata = Field(ObjectMeta)
    spec = Field(FiaasApplicationSpec)


class FiaasStatus(Model):
    """Deprecated. This model will be removed as soon as migration to ApplicationStatus is complete"""
    class Meta:
        url_template = "/apis/fiaas.schibsted.io/v1/namespaces/{namespace}/statuses/{name}"

    # Workaround for https://github.com/kubernetes/kubernetes/issues/44182
    apiVersion = Field(six.text_type, "fiaas.schibsted.io/v1")
    kind = Field(six.text_type, "Status")

    metadata = Field(ObjectMeta)
    result = Field(six.text_type)
    logs = ListField(six.text_type)


class FiaasApplicationStatus(Model):
    class Meta:
        url_template = "/apis/fiaas.schibsted.io/v1/namespaces/{namespace}/application-statuses/{name}"

    # Workaround for https://github.com/kubernetes/kubernetes/issues/44182
    apiVersion = Field(six.text_type, "fiaas.schibsted.io/v1")
    kind = Field(six.text_type, "ApplicationStatus")

    metadata = Field(ObjectMeta)
    result = Field(six.text_type)
    logs = ListField(six.text_type)
