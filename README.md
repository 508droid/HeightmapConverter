# Heightmap Converter

Hey there! Welcome to the Heightmap Converter tool. This program lets you take a greyscale image and turn it into a heightmap array, perfect for noise generation in your projects. We’ve packed in a ton of features to make your life easier. Let’s dive in!

## Features

### 1. **Graphical User Interface (GUI)**
Load your images, tweak settings, and save your heightmaps all in one place.

### 2. **Optional Preprocessing**
Got a huge image? No problem. You can choose to resize it to make processing quicker. Plus, it’s grayscale conversion all the way, keeping things simple and effective.

### 3. **Customizable Preprocessing Size**
Set your preprocessing size in pixels or percentages for both width and height. Just select the unit from the dropdown menu and input the desired value.

### 4. **Scale and Offset Adjustment**
Need your mountains a bit higher or valleys a bit deeper? Adjust the height scale and offset right from the GUI.

### 5. **Preview Heightmap**
Before you commit to saving, preview your heightmap. We’ve integrated a simple but powerful preview feature using matplotlib.

### 6. **Multiple Export Formats**
Flexibility is key. Save your heightmap in Lua, CSV, or JSON format. Whatever floats your boat.

### 7. **Logging**
Keep track of everything that’s going on with our handy logging feature. Every action and error is recorded in the log window.

### 8. **Progress Bar**
No more wondering how long something will take. The progress bar shows you the status of loading, processing, and saving tasks.

### 9. **Threading**
We’ve implemented threading to keep the GUI responsive, even when processing large images or saving big heightmaps.

### 10. **Chunked Processing**
Processing and saving large images can be a nightmare. We handle this by processing and saving in smaller chunks, making it efficient and crash-proof.

## Getting Started

### Prerequisites
You’ll need Python installed. Make sure you’ve got these libraries too:

```bash
pip install pillow numpy matplotlib
```

### Running the Tool
1. **Clone the repository:**
   ```bash
   git clone https://github.com/508droid/HeightmapConverter
   cd heightmap-converter
   ```

2. **Run the script:**
   ```bash
   python heightmap_converter.py
   ```

3. **Load an image:**
   Click the “Load Image” button and select your map image (JPEG or PNG).

4. **Adjust settings:**
   Set your desired height scale and offset using the entries provided. If you enable preprocessing, set the desired width and height values and units (pixels or percentages).

5. **Process the image:**
   Hit “Process Image” and let the magic happen.

6. **Preview your heightmap:**
   Click “Preview Heightmap” to see how it looks.

7. **Save your heightmap:**
   Choose your format (Lua, CSV, or JSON) and save it to your desired location.

## Contributing

Got ideas? Found a bug? Feel free to fork the repo and submit a pull request.
