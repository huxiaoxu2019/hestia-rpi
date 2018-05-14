PID = $(shell ps -ef | grep 'main.py' | grep -v 'grep' | awk '{print $$2}')

init:
	pip install -r requirements.txt

start:
	@nohup hestia/main.py > hestia/console &

stop:
	@echo ${PID}
	@echo "current hestia pid is:${PID}"
	@if [ $(PID) -gt 0 ]; \
		then \
		`kill -9 $(PID)`; \
        echo "hestia rpi(pid ${PID}) has been stopped."; \
    else \
	    echo "no rpi server running."; \
	fi

test:
	nosetests tests
