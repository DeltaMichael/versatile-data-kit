/*
 * Copyright (c) 2021 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

package com.vmware.taurus.service.model;

import com.vmware.taurus.controlplane.model.data.DataJobResources;
import lombok.Data;

/**
 * Store this in the database if the data job configuration could not or should not
 * be retrieved from the kubernetes manifest of the data job deployment like Airflow DAG locations.
 */
@Data
public class JobDeployment {

   private String dataJobName;

   private String gitCommitSha;

   private String imageName;

   private String cronJobName;

   private Boolean enabled;

   private String mode;

   private DataJobResources resources;
}