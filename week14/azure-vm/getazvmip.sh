#!/bin/bash
az vm show --resource-group 2021-fall-tdarlington-rg --name Tom-VM -d --query [publicIps] -o tsv