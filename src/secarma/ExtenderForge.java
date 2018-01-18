package secarma;

import burp.IBurpExtenderCallbacks;

/**
 * This is a convenience class making certain items truly global while running.
 * If we want to access the extension name we can call "ExtenderForge.ExtensionName"
 * For example. 
 * 
 * @author cornerpirate
 */
public class ExtenderForge {

    public static IBurpExtenderCallbacks callbacks;
    public static ExtenderForgeGui customDecoderGui;
    public static String ExtensionName = "Extender Forge" ;
}
