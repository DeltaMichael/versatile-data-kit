# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import json
import os

import tornado
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join

from .vdk_ui import VdkUI


class RunJobHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({"path": f"{os.getcwd()}"}))

    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()
        status_code = VdkUI.run_job(input_data["jobPath"], input_data["jobArguments"])
        self.finish(json.dumps({"message": f"{status_code}"}))


class DeleteJobHandler(APIHandler):
    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()
        try:
            status = VdkUI.delete_job(
                input_data["jobName"], input_data["jobTeam"], input_data["restApiUrl"]
            )
            self.finish(json.dumps({"message": f"{status}", "error": ""}))
        except Exception as e:
            self.finish(json.dumps({"message": f"{e}", "error": "true"}))


class DownloadJobHandler(APIHandler):
    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()
        try:
            status = VdkUI.download_job(
                input_data["jobName"],
                input_data["jobTeam"],
                input_data["restApiUrl"],
                input_data["parentPath"],
            )
            self.finish(json.dumps({"message": f"{status}", "error": ""}))
        except Exception as e:
            self.finish(json.dumps({"message": f"{e}", "error": "true"}))


class CreateJobHandler(APIHandler):
    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()
        try:
            local = True if input_data["isLocal"] else False
            cloud = True if input_data["isCloud"] else False
            status = VdkUI.create_job(
                input_data["jobName"],
                input_data["jobTeam"],
                input_data["restApiUrl"],
                input_data["jobPath"],
                local,
                cloud,
            )
            self.finish(json.dumps({"message": f"{status}", "error": ""}))
        except Exception as e:
            self.finish(json.dumps({"message": f"{e}", "error": "true"}))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    run_job_route_pattern = url_path_join(base_url, "vdk-jupyterlab-extension", "run")
    run_job_handlers = [(run_job_route_pattern, RunJobHandler)]
    web_app.add_handlers(host_pattern, run_job_handlers)

    delete_job_route_pattern = url_path_join(
        base_url, "vdk-jupyterlab-extension", "delete"
    )
    delete_job_handlers = [(delete_job_route_pattern, DeleteJobHandler)]
    web_app.add_handlers(host_pattern, delete_job_handlers)

    download_job_route_pattern = url_path_join(
        base_url, "vdk-jupyterlab-extension", "download"
    )
    download_job_handlers = [(download_job_route_pattern, DownloadJobHandler)]
    web_app.add_handlers(host_pattern, download_job_handlers)

    create_job_route_pattern = url_path_join(
        base_url, "vdk-jupyterlab-extension", "create"
    )
    create_job_handlers = [(create_job_route_pattern, CreateJobHandler)]
    web_app.add_handlers(host_pattern, create_job_handlers)
