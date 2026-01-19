<h1>Oil spill simulation at Bay City</h1>

<p> <b>INF202: Project task in advanced programming January 2026</b></p>
<p><b>@University of Life Sciences </b></p><img src="https://github.com/Suilerac/INF202---Group-18/raw/main/gifs_and_pictures/NMBU.jpg" alt="NMBU logo" width="200" height="200">

<ul>
<b>Made by Group-18</b>
    <li>Håkon Bekken (Realhaakon)</li>
    <li>Andreas Carelius Brustad (Suilerac)</li>
    <li>Johannes Husevåg Standal (JohannesStandal)</li>  
</ul>

<h1> Introduction </h1>


<h1> Installation & user guide </h1>
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

<h1> How to use the simulation </h1>

More 