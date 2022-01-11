#!/bin/bash

tmpPath=$(get_octopusvariable "Octopus.Action.Package[appsecMonitor].ExtractedPath")

#clean up pipeline artifacts
rm $tmpPath/PACKAGE.txt
rm $tmpPath/RELEASE_VERSION.txt
rm $tmpPath/bitbucket-pipelines.yml
rm $tmpPath/deploy.sh

#deploy
cp -R $tmpPath/* #{appsecMonitorRootPath}

#fix permissions
cd #{appsecMonitorRootPath}
find #{appsecMonitorRootPath} -name "*.sh" -type f -not -path '*/\.*' -exec chmod o-rwx {} \; -exec chmod ug+rwx {} \;
mkdir -p #{appsecMonitorRootPath}/out
mkdir -p #{appsecMonitorRootPath}/out/dasthealth
mkdir -p #{appsecMonitorRootPath}/out/sasthealth
mkdir -p #{appsecMonitorRootPath}/out/sastfindings
mkdir -p #{appsecMonitorRootPath}/out/sastfindings/cxReports
chmod -R o-rwx #{appsecMonitorRootPath}
chmod ug+rwx #{appsecMonitorRootPath}/run_fullmonitor
chmod ug+rwx #{appsecMonitorRootPath}/run_sastmonitor
chmod ug+rwx #{appsecMonitorRootPath}/out
chmod ug+rwx #{appsecMonitorRootPath}/out/dasthealth
chmod ug+rwx #{appsecMonitorRootPath}/out/sasthealth
chmod ug+rwx #{appsecMonitorRootPath}/out/sastfindings
chmod ug+rwx #{appsecMonitorRootPath}/out/sastfindings/cxReports
sudo mv #{appsecMonitorRootPath}/run_sastmonitor /etc/cron.daily
sudo mv #{appsecMonitorRootPath}/run_fullmonitor /etc/cron.weekly