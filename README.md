# Rhino WebView with Custom URI Schemes

This guide demonstrates how to integrate an HTML slider into Rhino using the `Eto.Forms.WebView` control, and how to intercept custom URI schemes to handle communication between JavaScript (in the web view) and IronPython (in Rhino). The interaction allows Rhino to capture changes from the web interface, making it easier to create dynamic tools.

**Disclaimer**: This implementation was created with substantial assistance from OpenAI's ChatGPT.

---

## The Goal

We’re embedding an HTML slider inside a Rhino form using `Eto.Forms.WebView`. When the user moves the slider, it triggers a JavaScript event that sends a custom URI scheme (`greenscenario`) back to Rhino. Rhino intercepts this URI and extracts the value of the slider to process further.

---

## Step-by-Step Explanation

### Step 1: Creating the Form

First, we create a simple Rhino form using `Eto.Forms`. The form includes a `WebView` to display HTML content. 

```python
class GreenScenarioPanel(Form):
    def __init__(self):
        self.Title = "Green Scenario WebView"
        self.ClientSize = Size(800, 600)
```

- `Form`: This creates a new window in Rhino.
- `Title`: Sets the title of the form window.
- `ClientSize`: Defines the window size (800x600 pixels).

### Step 2: HTML Content for the WebView

We then define the HTML content that will be loaded into the WebView. It includes a slider element (`<input type='range'>`) and some JavaScript that listens for the slider's `input` event.

```python
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
```

- **HTML**: Displays a slider with values from 0 to 100.
- **JavaScript**: Listens for slider movements (the `input` event) and updates the custom URI scheme with the current value.

### Step 3: Loading HTML into WebView

Now we create the `WebView` control and load the HTML content from Step 2 into it.

```python
self.webview = WebView()
self.webview.Size = Size(800, 600)
self.webview.LoadHtml(html)
```

- `WebView`: Displays the web content (our HTML with the slider).
- `LoadHtml`: Loads the HTML string into the `WebView`.

### Step 4: Intercepting the Custom URI Scheme

This part handles the navigation event when JavaScript tries to navigate to the custom URI (`greenscenario`). Rhino will catch it and prevent actual navigation.

```python
self.webview.DocumentLoading += self.on_document_loading
```

This code ensures that every time the `WebView` tries to load a new document (in this case, the custom URI), the `on_document_loading` method is triggered.

```python
def on_document_loading(self, sender, e):
    if e.Uri.Scheme == "greenscenario":
        e.Cancel = True  # Prevent navigation
        value = e.Uri.Query.strip('?')  # Extract slider value
        self.communicate_with_webview(value)
```

- `e.Cancel = True`: This prevents the `WebView` from navigating away.
- `e.Uri.Query.strip('?')`: Extracts the value of the slider from the query string (e.g., `?50` becomes `50`).
- `communicate_with_webview(value)`: Passes the slider value to the method that handles communication between the web view and Rhino.

### Step 5: Logging the Slider Value in Rhino

Finally, we log the slider value to Rhino's command line or output panel using `RhinoApp.WriteLine`:

```python
def communicate_with_webview(self, value):
    Rhino.RhinoApp.WriteLine("Slider Value: {0}".format(value))
```

This ensures that every time the slider is moved, the value is displayed in Rhino’s output.

---

## Summary

With this setup, you can create a simple Rhino form that embeds a web-based slider and communicates with Rhino via a custom URI scheme. The form intercepts the slider’s movements and logs the value, opening up the possibility to extend this to more complex functionality in Rhino.

If you're wondering why this works: JavaScript in the `WebView` triggers navigation to a custom URI (`greenscenario`), Rhino intercepts that URI via the `DocumentLoading` event, and then extracts the relevant data (the slider value) to process it inside the form.
