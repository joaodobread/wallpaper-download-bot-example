from selenium.webdriver import Chrome


class BaseBot(Chrome):
    def wait_to_load(self):
        started_load_at = time()
        while self.execute_script("return document.readyState") != "complete":
            if started_load_at > self.default_delay:
                raise Exception("Wait time exced")

    def run():
        raise NotImplementedError()