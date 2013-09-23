#!/usr/bin/python

import getopt
import sys
import os
import jenkins
import urllib2

TEMPLATE_CONFIG = "./config.xml.template"


def usage():
    print ("""Usage: %s
           [-h|--help]
           [-s|--server] <Jenkins server>[:port]
           [-n|--name] <Repository name>
           [-p|--project-url] <Github project URL>
           [-g|--git-url] <Git URL>
           [-c | --component] <Build system component>""" %
           os.path.basename(__file__))


def new_config(template, name, project_url, git_url, component):
    with open(template, 'r') as in_file:
        contents = in_file.read()
        contents = contents.replace("@@@GIT_NAME@@@", name)
        contents = contents.replace("@@@PROJECT_URL@@@", project_url)
        contents = contents.replace("@@@GIT_URL@@@", git_url)
        contents = contents.replace("@@@BUILD_SYSTEM_COMPONENT@@@", component)
    return contents


def new_jenkins_job(server, name, project_url, git_url, component):
    print "Creating new Jenkins Github Pull Request Builder job for %s" % name
    print "Creating build config...",
    config = new_config(TEMPLATE_CONFIG, name, project_url, git_url, component)
    print "Done"
    try:
        print "Accessing Jenkins on server '%s'" % server,
        j = jenkins.Jenkins(server)
        print "Done"
        print "Creating new Jenkins job...",
        j.create_job(name, config)
        print "Done"
    except urllib2.URLError, e:
        print "Error connecting to Jenkins API: %s." % e
    except jenkins.JenkinsException, e:
        print "Error creating new job: %s." % e


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:n:p:g:c:",
                                   ["help", "server=", "name=", "project-url=",
                                    "git-url=", "component="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)
        usage()
        sys.exit(2)
    server = name = project_url = git_url = component = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--server"):
            server = a
        elif o in ("-n", "--name"):
            name = a
        elif o in ("-p", "--project-url"):
            project_url = a
        elif o in ("-g", "--git-url"):
            git_url = a
        elif o in ("-c", "--component"):
            component = a
        else:
            assert False, "unhandled option"
    if None in (server, name, project_url, git_url, component):
        usage()
        sys.exit(2)
    new_jenkins_job(server, name, project_url, git_url, component)


if __name__ == "__main__":
    main()
