<h1>Bay city oil spill simulation</h1>

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
$pip install uv
$uv venv
# activate local venv
$uv venv/bin/activate  
# install dependencies
$uv pip install -r requirements.txt
# build a distribution and install our package
$uv build
$uv pip install .\dist\inf202_group_18-0.1.0-py3-none-any.whl
</pre>



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
<li>Examples  # Contains examples.</li>
<li>Config    #toml configuration files</li>
<li>gifs_and_pictures</li>
<li>meshes    #Contains maps with meshes</li>
<li>Report
<li>src: <b>See UML diagram</b></li> <ul>
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
<li>temp      #temprorary folder for image creation</li>
<li>Tests     #Tests for all classes</li>

</ul>

<img src="https://github.com/Suilerac/INF202---Group-18/raw/main/gifs_and_pictures/UML-diagram-final.jpg" alt="UML-diagram" width="1000" height="1000">




<h1> User guide  </h1>
<p>
Hello and welcome to our user guide, showing the simulation and its possibilities.    
Follow the installation guide on github, and use the virtual enviroment as the interpeter.  </p>

Bellow is the input.toml file. The simulation takes in the following arguments in order to run. 

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
">[settings]
nSteps = 100 #number of time steps
tEnd = 0.5 #Specific end time (MUST BE FLOAT value)

[geometry]
meshName = "meshes/bay.msh" #name of computational 
borders = [[0.0, 0.45], [0.0, 0.2]] # boarders of fishing grounds

[IO]
logName = "input.log" #name of logfile
writeFrequency = 20 #frequency of output video.</pre> 

Execute the following command in terminal to run one specific config file
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
">python main.py -f configs .\configs\"Specific config file"</pre>


Execute the following command in terminal to run multiple config files  
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
">
python main.py -f configs --find_all</pre>

<p>
The simulation will be stored in a newly created folder with the specific name you gave the .toml file. 
It will output the following files: 

</p>
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
"><b>Inside the folder created after simulation</b>
-> "name_of_config_file".log # Display oil density in fishing grounds 
-> "name_of_config_file".mp4 # A video showing the simulation
-> "name_of_config_file".png # The last picture generated by the simulaton</pre>

Running <b>main.py</b> will use input.toml as configuration file. 

<h1>
Here are some example simulations with following paramaters </h1>

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
"><b>The Bay city default simulation from task description </b>

[settings]
nSteps = 500
tEnd = 0.5 

[geometry]
meshName = "meshes/bay.msh" 
borders = [[0.0, 0.45], [0.0, 0.2]]

[IO]
logName = "default.log"
writeFrequency = 20 .</pre> 

<img src="https://github.com/Suilerac/INF202---Group-18/raw/main/gifs_and_pictures/default.gif" alt="Default simulation" width="1000" height="1000">


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
"><b>simpleMesh example</b>

[settings]
nSteps = 1500
tEnd = 3.0

[geometry]
meshName = "meshes/simple.msh"
borders = [[0.0, 0.45], [0.0, 0.2]]

[IO]
logName = "simple.log"
writeFrequency = 10</pre> 

<img src="https://github.com/Suilerac/INF202---Group-18/raw/main/gifs_and_pictures/simple.gif" alt="simple mesh simulation" width="1000" height="1000">



<h1>Results</h1>

<p>In conclusion, we got the following results with a few select simulations:</p>

<table border="1" cellspacing="0" cellpadding="6" style="border-collapse:collapse; text-align:center; margin:auto;">
  <tr>
    <th></th>
    <th>Default</th>
    <th>Longer duration</th>
    <th>Fewer steps</th>
  </tr>
  <tr>
    <td><b>nSteps</b></td>
    <td>500</td>
    <td>2500</td>
    <td>5</td>
  </tr>
  <tr>
    <td><b>tEnd</b></td>
    <td>0.5</td>
    <td>2.5</td>
    <td>0.5</td>
  </tr>
  <tr>
    <td><b>meshName</b></td>
    <td>bay.msh</td>
    <td>bay.msh</td>
    <td>bay.msh</td>
  </tr>
  <tr>
    <td><b>borders</b></td>
    <td>[[0.0, 0.45], [0.0, 0.2]]</td>
    <td>[[0.0, 0.45], [0.0, 0.2]]</td>
    <td>[[0.0, 0.45], [0.0, 0.2]]</td>
  </tr>
  <tr>
    <td><b>logName</b></td>
    <td>log</td>
    <td>log</td>
    <td>log</td>
  </tr>
  <tr>
    <td><b>writeFrequency</b></td>
    <td>20</td>
    <td>10</td>
    <td>1</td>
  </tr>
  <tr>
    <td><b>Oil density in fishing grounds at end</b></td>
    <td>19.33</td>
    <td>35.84</td>
    <td>32.13</td>
  </tr>
  <tr>
    <td><b>Runtime on Macbook Air M4</b></td>
    <td>2.7s</td>
    <td>20.6s</td>
    <td>0.6s</td>
  </tr>
</table>

<p>There were some interesting observations about the two last items. 
The default values ran as expected, concluding with oil hitting the fishing grounds. 
If we let it go to <code>tEnd = 2.5</code>, as seen in the "Longer Duration" case, 
the oil density in the fishing grounds stabilized at <b>35.84</b>. 
This occurred because as the oil hits the mesh borders, the flow stops—line cells 
cannot give or receive oil.</p>

<p>The results of the "Fewer steps" simulation were also interesting. 
The oil density rapidly grew across the entire plot, leaving it almost completely covered in oil by the end. 
This happened because the <code>dt</code> variable grew so large that the oil density increased beyond reasonable values.</p>

<p>The entire project resulted in a highly scalable, well-structured, and optimized package. 
Adding a new cell type is as simple as creating a subclass of <code>Cell</code> and implementing 
its <code>area</code> calculation. Then, add the new class to the <code>types</code> dictionary in 
<code>CellFactory</code>. All other mathematical operations and data are generalized for all convex polygons.</p>

<p>The code structure is intuitive, allowing a full simulation with custom parameters to be run in just a few lines. 
Data handling is organized logically: geometric data related to cells is handled in <code>Cell</code>; 
mesh-wide operations reside in <code>Mesh</code>; simulation control lives in <code>Simulation</code>; 
visualization in <code>Plotter</code>; and numerical solving in <code>Solver</code>. 
This modular design makes the system easy to read, maintain, and extend.</p>

<p>We also focused on performance optimization. A single simulation runs in under 5 seconds on our test machine, 
allowing for rapid iteration and effective debugging with minimal downtime.</p>

<img src="https://github.com/Suilerac/INF202---Group-18/raw/main/gifs_and_pictures/default.jpg" alt="LastPictureDefaultSim" width="1000" height="1000">
