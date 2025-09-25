
# 3D Avatar

In this phase, we aimed to develop a real-time lip-sync system that can be integrated with a MetaHuman character in Unreal Engine. 

We decide to use Nvidia Omniverse Audio2Face which supports real-time streaming via Live Link plugin.


## Installation

1- Install Epic Games Launcher & Unreal Engine UE5.3

2- Install Visual Studio 2022

3- Install NVIDIA Omniverse Launcher

4- inside NVIDIA Omniverse Launcher Install audio2face-2023.2.1

5- Python >= 3.8

    
## Usage
download this zip file https://drive.google.com/file/d/1nX88JmIGyKnesIvr48haR6t4Z9vmSRnv/view?usp=sharing then extract the file into `Content`
### Edit configurations
#### 1- 🗂 run_headless_a2f.py
In the code, you will find a line like this:

```
bat_file_path = (
    r"C:\Users\EjadaAi\AppData\Local\ov\pkg\audio2face-2023.2.0\audio2face_headless.bat"
)
```
⚠️ You must edit this path to match where Audio2Face is installed on your laptop.

You can find the correct path by navigating in File Explorer to:
```
C:\Users\<YourUserName>\AppData\Local\ov\pkg\
```



#### 2- 🗂 set_a2f.py

In the code, you will see a line like this:

```python
usd_file_path = r"D:\af\claire_solved_arkit\claire_solved_arkit.usd"
```
⚠️ You must edit this path to point to the .usd file on your own system.

you will find the following line:

```python
root_path_result = client.set_root_path(client.players_available, "D:/Avatar/audios")
```
👉 “You need to change the path `D:/Avatar/audios` to the path on your computer that contains the audio files.

**Note** 

I set the audio files path as a static path in `set_a2f.py` to improve latency.

If you want to make it a dynamic path, remove this line and the following two lines in `run_audio.py` 

```python
directory = file_path.rsplit('/', 1)[0]

client.set_root_path(players_available, directory)
```

#### 3- 🗂 run_audio.py
In the code, you will see something like this:

```python
CONFIG_FILE = os.path.join(
    r"D:\Unreal Projects\AvatarCPP7\Scripts", "audio_config.json"
)
```
⚠️ You must edit this path to match the location of your audio_config.json file.



#### 4. 🗂 run_audio_helper.bat file

Inside `run_audio_helper.bat`, you will see a line like this:

```bat
pythonw "D:\Unreal Projects\AvatarCPP7\Scripts\run_audio.py"
```
⚠️ You must edit the path so it matches the location of your run_audio.py file.

#### 5. 🗂 game.bat file
Inside `game.bat`, you will see lines like this:

```bat
python "D:\Unreal Projects\AvatarCPP7\Scripts\run_headless_a2f.py"
python "D:\Unreal Projects\AvatarCPP7\Scripts\set_a2f.py"
start "" "D:\Unreal Projects\AvatarCPP7\package\Windows\AvatarCPP7.exe"
```
⚠️ You must edit these paths so they match your own project directory.

#### 5- 🗂 game - Copy.bat file
Inside `game - Copy.bat`, you will see lines like this:

```bat
python "D:\Unreal Projects\AvatarCPP7\Scripts\run_headless_a2f.py"
python "D:\Unreal Projects\AvatarCPP7\Scripts\set_a2f.py"
```
⚠️ You must edit these paths so they match your own project directory.

**Note** 
👉 I use this file during development and testing, but game.bat runs the packaged Unreal project.

### Execute game - Copy.bat file
to launch audio2face_headless and configure the settings 

### Launch Unreal Engine 
#### 1- Open Unreal Project .uproject
#### 2- In the **Content Browser**, navigate to:
    Content/Stylized_Egypt/Maps/
#### 3- Open the **mainmenumap** level.
#### 4- Enable necessary plugins
From Edit -> Plugins
- NVIDIA Omniverse ACE: Audio2Face
- Easy File Dialog
- Json Blueprint Utilities
#### 5- Enable live coding
At the bottom toolbar, click the **Live Coding** icon:

*(Tooltip: **Recompiles and reloads C++ code**)*

#### 6- Open UploadAudio Widget Blueprint
In the **Content Browser**, navigate to:
```
Content/UI/UploadAudio/
```
Click on `Upload .wav` button the see tha `Details` Panel.

Scroll down and open `On Click` icon and the Event Graph will be opened.

You will find a node Called `Make FilePath` contains this path
```
D:\Unreal Projects\AvatarCPP7\Scripts\audio_config.json
```
⚠️ You must edit this path to match the location of your audio_config.json file.

#### 6- Open `UploadAudio` Widget Blueprint
In the **Content Browser**, navigate to:
```
Content/UI/UploadAudio/
```
Click on any button on the widget blueprint (e.g., `Upload .wav`) button and see the `Details` Panel.

Scroll down and open `On Click` icon and the Event Graph will be opened.

You will find a node Called `Make FilePath` contains this path
```
D:\Unreal Projects\AvatarCPP7\Scripts\audio_config.json
```
⚠️ You must edit this path to match the location of your audio_config.json file.

#### 7- Open `ChooseCharacter` Widget Blueprint
- In the **Content Browser**, navigate to:
```
Content/UI/ChooseCharacter/
```
- Click on any button on the widget blueprint see the `Details` Panel.

- Scroll down and open `On Click` icon and the Event Graph will be opened.

- You will find a node Called `Run Batch File` contains this path
```
D:\Unreal Projects\AvatarCPP7\Scripts\run_audio_helper.bat
```
⚠️ You must edit this path to match the location of your run_audio_helper.bat file.


### play the game 
👉 Click the Play button (▶️) in the Unreal Editor toolbar to test the game.











## For creating new unreal project
you need some additional steps

1- Create Blank Game Project (C++)

**⚠️ Note**
Make sure you create a C++ project, not a Blueprint-only project.
Live Coding and the included scripts require a C++ setup to work correctly.

2- Choose Project Location and Project Name (e.g., `AvatarTest`)

3- Copy the following folders to the project location:

* Content
* Plugins
* Scripts 

4- Create Blueprint Function Library 

* In the top menu bar, click **Tools → New C++ Class...**
* Choose a parent class: `Blueprint Function Library`
* **Next → Create Class**

5- Copy the C++ code

- Open `Source\AvatarCPP7\MyBlueprintFunctionLibrary.h`

- Copy the contents into the .h file of the Blueprint Function Library you just created.

**⚠️Note**

In .h file of Blueprint Function Library you just created, you’ll see something like :

```
class AVATARTEST_API UMyBlueprintFunctionLibrary : public UBlueprintFunctionLibrary
```
`AVATARTEST_API` → a macro automatically generated by Unreal for your project.

- It makes the class exportable so Unreal Engine  can use it.

- The name **AVATARTEST_API** comes from your project’s name **AvatarTest**.
👉 When copying the C++ code, do not change or remove AVATARTEST_API. Leave it exactly as Unreal generated it.

👉 Your project will have its own macro name (e.g., MYPROJECT_API), which depends on your project’s name.

6- Follow the same steps described in the Usage section.

