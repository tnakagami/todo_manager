#!/bin/bash

readonly CURRENT_DIR=$(cd $(dirname $0) && pwd)
readonly TEST_COMPOSE_FILE=${CURRENT_DIR}/for_django_test/docker-compose_test.yml

# ================
# = main routine =
# ================
while [ -n "$1" ]; do
    case "$1" in
        ps )
            docker-compose ps
            shift
            ;;

        logs )
            docker-compose logs -t | sort -t "|" -k 1,+2d
            shift
            ;;

        stop | restart | down )
            exe_opt="$1"
            docker-compose ${exe_opt}
            shift
            ;;

        start )
            docker-compose up -d
            shift
            ;;

        build )
            docker-compose build
            # delete image of none
            docker images | grep '<none>' | awk '{print $3;}' | xargs -I{} docker rmi {}
            shift
            ;;

        test_build )
            docker-compose -f ${TEST_COMPOSE_FILE} build
            # delete image of none
            docker images | grep '<none>' | awk '{print $3;}' | xargs -I{} docker rmi {}
            shift
            ;;

        test_start )
            docker-compose -f ${TEST_COMPOSE_FILE} up -d
            shift
            ;;

        test_logs )
            docker-compose -f ${TEST_COMPOSE_FILE} logs test_django
            shift
            ;;

        test_down )
            docker-compose -f ${TEST_COMPOSE_FILE} down -v
            shift
            ;;

        -h | --help | --usage )
            echo "Usage: [for exec] $0 [build|start|stop|restart|down|ps|logs]"
            echo "       [for test] $0 [test_build|test_start|test_logs|test_down]"
            shift
            ;;

        * )
            shift
            ;;
    esac
done
