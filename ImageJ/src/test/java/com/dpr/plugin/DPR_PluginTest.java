package com.dpr.plugin;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DPR_PluginTest {
    @Test
    void pluginLoads() {
        // Basic test to ensure the plugin class can be instantiated
        assertDoesNotThrow(() -> new DPR_Plugin());
    }
} 