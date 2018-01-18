package burp;

import java.awt.Component;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTextArea;
import secarma.ExtenderForge;
import secarma.ExtenderForgeGui;

public class BurpExtender implements IBurpExtender, ITab {

    private IBurpExtenderCallbacks callbacks;
    private IExtensionHelpers helpers;
    private JSplitPane splitPane;
    private ExtenderForgeGui customDecoderGui;
    private JPanel panel;
    private JTextArea display;
    private JScrollPane scroll;
    private IHttpRequestResponse currentlyDisplayedItem;

    /**
     * Burp calls this to register ExtenderForge as an Extender 
     * @param callbacks
     */
    @Override
    public void registerExtenderCallbacks(final IBurpExtenderCallbacks callbacks) {

        ExtenderForge.callbacks = callbacks;
        // set our extension name
        callbacks.setExtensionName(ExtenderForge.ExtensionName);
        ExtenderForge.customDecoderGui = new ExtenderForgeGui();
        callbacks.addSuiteTab(this);
        // obtain an extension helpers object
        helpers = callbacks.getHelpers();
    }

    @Override
    public String getTabCaption() {
        return ExtenderForge.ExtensionName;
    }

    @Override
    public Component getUiComponent() {
        return ExtenderForge.customDecoderGui;
    }

}
