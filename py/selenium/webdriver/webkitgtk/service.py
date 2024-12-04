# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import warnings
from typing import List
from typing import Mapping
from typing import Optional

from selenium.webdriver.common import service

DEFAULT_EXECUTABLE_PATH: str = "WebKitWebDriver"


class Service(service.Service):
    """A Service class that is responsible for the starting and stopping of
    `WPEWebDriver`.

    :param executable_path: install path of the WebKitWebDriver executable, defaults to `WebKitWebDriver`.
    :param port: Port for the service to run on, defaults to 0 where the operating system will decide.
    :param service_args: (Optional) List of args to be passed to the subprocess when launching the executable.
    :param log_output: (Optional) File path for the file to be opened and passed as the subprocess stdout/stderr handler.
    :param env: (Optional) Mapping of environment variables for the new process, defaults to `os.environ`.
    """

    def __init__(
        self,
        executable_path: str = DEFAULT_EXECUTABLE_PATH,
        port: int = 0,
        log_path: Optional[str] = None,
        log_output: Optional[str] = None,
        service_args: Optional[List[str]] = None,
        env: Optional[Mapping[str, str]] = None,
        **kwargs,
    ) -> None:
        self.service_args = service_args or []
        if log_path is not None:
            warnings.warn("log_path is deprecated, use log_output instead", DeprecationWarning, stacklevel=2)
            log_path = open(log_path, "wb")
        log_output = open(log_output, "wb") if log_output else None
        super().__init__(
            executable_path=executable_path,
            port=port,
            log_output=log_path or log_output,
            env=env,
            **kwargs,
        )

    def command_line_args(self) -> List[str]:
        return ["-p", f"{self.port}"] + self.service_args
