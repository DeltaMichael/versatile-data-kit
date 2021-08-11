/*
 * Copyright (c) 2021 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

package com.vmware.taurus.service.credentials;

import org.junit.Assert;
import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.util.Optional;

/**
 * TODO: enable it in CICD:
 * apk --no-cache add krb5
 * + pointing to the krb5.conf
 * + using hadoop-minikdc or docker KDC server
 */
public class KerberosCredentialsServiceTestManual {

    @Test
    public void test() throws IOException {
        String kadminUser = System.getProperty("kadmin_password", "phuser/admin");
        String kadminPassword = System.getProperty("kadmin_password");

        Assumptions.assumeTrue(kadminPassword != null && !kadminPassword.isBlank(),
                "kadmin_password is missing. Assuming test is disabled.");

        KerberosCredentialsRepository service = new KerberosCredentialsRepository(kadminUser, kadminPassword);

        File file = File.createTempFile("keytab_test", ".keytab");
        file.deleteOnExit();

        String principal = "taurus-pipelines-test-user";
        service.deletePrincipal(principal);
        Assert.assertEquals(false, service.principalExists(principal));
        service.createPrincipal(principal, Optional.of(file));
        Assert.assertEquals(true, service.principalExists(principal));
        Assert.assertTrue(file.exists());
        Assert.assertTrue(file.length() > 0);
        service.deletePrincipal(principal);
        Assert.assertEquals(false, service.principalExists(principal));
    }

}