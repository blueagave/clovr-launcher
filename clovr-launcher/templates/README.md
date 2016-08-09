# CloVR EC2 VM Launcher Web Application

A web application that can launch the CloVR VM on EC2 in cloud-only mode. Designed to mimic the current workflow of the DIAG Computings 
launch VM appliance.

Web design and functionality based off of the [Start Boostrap](http://startbootstrap.com/) - [Simple Sidebar](http://startbootstrap.com/template-overviews/simple-sidebar/) theme with inspiration taken from the [INISPIA Admin Theme](https://wrapbootstrap.com/theme/inspinia-responsive-admin-theme-WB0R5L90S)

## Getting Started

To use this web application the Dockerfile in the root directory of this repository should be run to build a docker container containing all dependencies.

From there the container should be run using docker and the web application should be accessed at the DOCKERVM IP Address.
