#!/usr/bin/env python3
from aws_cdk.core import App
from cdk_code.my_cdk_stack import MyCdkStack

app = App()
MyCdkStack(app, "MyCdkStack")

app.synth()