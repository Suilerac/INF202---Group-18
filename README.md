<h1>Oil spill simulation at Bay City</h1>

<p> <b>INF202: Project task in advanced programming January 2026</b></p>
<p><b><a href="https://www.nmbu.no/">@University of Life Sciences </b></a></p><img src="https://github.com/Suilerac/INF202---Group-18/raw/main/gifs_and_pictures/NMBU.jpg" alt="NMBU logo" width="200" height="200">

<ul>
<b>Made by Group-18</b>
    <li>Håkon Bekken (Realhaakon)</li>
    <li>Andreas Carelius Brustad (Suilerac)</li>
    <li>Johannes Husevåg Standal (JohannesStandal)</li>  
</ul>

<h1> Introduction </h1>

Computer simulations are widely used in science and engineering to model complex systems and phenomena. 
They allow researchers to analyze and predict the behavior of systems under various conditions,
providing insights that may be difficult or impossible to obtain through traditional experimental methods.
The problem given of an oil spill has a real world implementation and are of significant for environmental concern. There are multiple examples like the <a href="https://pubs.acs.org/doi/10.1021/es5012862"> Deepwater Horizon oil spill</a> in 2010, where computational simulations was crucial in order to predict where surface oil would go, aiding skimming, booming, and shoreline protection.

Our simulation aims to model oil trajectory and spread forecasting in Bay city.
Outside Bay city is a fishing ground that are voulnerable to oil spills.
This report will discuss the mathematical models used to represent the oil spill dynamics,
the numerical methods to solve these models, and the implementation of the simulation.

<h1> Installation</h1>
<p>In this entry we will discuss the setup and usage instructions for our simulation. 
It will guide you from installation to actually simulating oil trajectory.
</p>

1. Select a folder, or create one (not /system32). Once you're in that folder, you can right-click it and select, 'Open in Terminal'

2. Clone the repository to your folder:
<pre style="background: #0d1117; 
color: #c9d1d9; 
padding: 16px; 
border-radius: 6px; 
font-family: 'Monaco', 'Menlo', monospace; 
font-size: 14px; 
margin: 8px 0; 
overflow-x: auto; 
white-space: pre;">
<span style="color: #58a6ff;">$</span> git clone https://github.com/Suilerac/INF202---Group-18.git
<span style="color: #58a6ff;">$</span> cd INF202---Group-18
</pre>


3. Set up a local venv. Inside CMD, make sure you are in the INF202--Group-18 folder

<pre style="
background: #0d1117;
color: #c9d1d9;
border: none;
padding: 16px;
border-radius: 6px;
font-family: 'Monaco','Menlo',monospace;
font-size: 14px;
line-height: 1.5;
width: 100%;
max-width: 600px;
resize: none;
margin: 8px 0;
tab-size: 4;
"># create virtual environment
python -m venv venv
# activate local venv
source venv/bin/activate  
# install dependencies
pip install -r requirements.txt</pre>



4. Download and install 3rd-party dependencies
- FFMPEG for windows
<div style="background: #0d1117; padding: 16px; border-radius: 6px; margin: 8px 0;">
  <a href="https://www.gyan.dev/ffmpeg/builds/" style="...same styles as above...">📥 Download FFmpeg</a>
  
Get version 8.0.1 ffmpeg-release-full.7z

Create a folder in your C: drive and name it <b>ffmpeg</b>

Unpack content from the download to the folder newly created.


<b>Edit system variables:</b>
Advanced system setting -> system variables ->  click<b> path</b> -> add new ->

copy paste this 
 
<b>C:\ffmpeg\ffmpeg-8.0.1-full_build\bin </b>

<b>ok </b> your way out. Verify install

Open a terminal and write <b> ffmpeg -version </b>

Hopefully it will display:

<b>ffmpeg version 8.0.1-full_build-www.gyan.dev Copyright (c) 2000-2025 the FFmpeg developers</b>
</div>

- FFmpeg for Mac
<div style="background: #0d1117; padding: 16px; border-radius: 6px; margin: 8px 0;">
Install homebrew (if you dont have it)

Open a terminal and
run: <b> brew install ffmpeg</b>

finally verify with <b>ffmpeg -version</b>
</div>

<h1> Folder Structure </h1>
<ul>
<li>Examples: Contains examples..</li>
<li>Config</li>
<li>gifs_and_pictures</li>
<li>meshes</li>
<li>src: <b>read UML diagram relationships</b>></li> <ul>
<li> Geometry Package</li> <ul>
<li> cellfactory.py</li>
<li> cells.py</li>
<li> line.py</li>
<li> mesh.py</li>
<li> triangle</li>
</ul>
<li> Simulation</li> <ul>
<li> plotter.py</li>
<li> simulation.py</li>
<li> solver.py</li>
</ul>
<li> InputOutput</li> <ul>
<li> commandlineParser.py</li>
<li> log.py</li>
<li> tomlParser.py</li>
</ul>
</ul>
<li>Tests </li>

</ul>


<h1> User guide  </h1>

Help me boys