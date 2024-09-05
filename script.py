import clr
clr.AddReference("Eto")
clr.AddReference("Rhino.UI")
from Eto.Forms import WebView, Form, DynamicLayout
from Eto.Drawing import Size, Padding
import Rhino

class GreenScenarioPanel(Form):
    def __init__(self):
        self.Title = "Green Scenario WebView"
        self.ClientSize = Size(800, 600)

        # HTML content with the slider input
        html = """
        <head>
            <meta http-equiv='X-UA-Compatible' content='IE=edge' />
            <title>Rhino UI</title>
        </head>
        <body>
            <p>Runoff limit
                <input type='range' min='0' max='100' value='50' class='slider' id='runoffLimit'>
            </p>
            <script>
                document.getElementById('runoffLimit').addEventListener('input', function() {
                    let value = document.getElementById('runoffLimit').value;
                    window.location = 'greenscenario:runofflimit?' + value;
                });
            </script>
        </body>
        """

        # Create the WebView control
        self.webview = WebView()
        self.webview.Size = Size(800, 600)
        self.webview.LoadHtml(html)

        # Subscribe to the DocumentLoading event to intercept navigation
        self.webview.DocumentLoading += self.on_document_loading

        # Create a DynamicLayout for the UI
        layout = DynamicLayout(DefaultSpacing=Size(5, 5), Padding=Padding(0))
        layout.AddSeparateRow(self.webview)
        layout.Add(None)
        
        # Set the layout as the content of the form
        self.Content = layout

    def on_document_loading(self, sender, e):
        # Intercept custom scheme (e.g., "greenscenario")
        if e.Uri.Scheme == "greenscenario":
            e.Cancel = True  # Prevent actual navigation
            value = e.Uri.Query.strip('?')  # Get the value from the query string
            self.communicate_with_webview(value)

    def communicate_with_webview(self, value):
        # Log the slider value to the Rhino command line or output panel
        Rhino.RhinoApp.WriteLine("Slider Value: {0}".format(value))

# Show the form
form = GreenScenarioPanel()
form.Show()
