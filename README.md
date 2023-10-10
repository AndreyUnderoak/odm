
  # ODM 2d Mapping Package
  ODM is a library that provides various of transformations from list of photo to maps with geo data, pointcloud, elevation maps. This package was created for 2d mapping from several images using python script and remote node. Also we have python script to take geo info and visualise it on map that odm has created.  
  
  ## Stages 🚀  
  There are 4 main "stages":
  
  0. Dataset: if you have not JPEG images with geo meta data in them, you need rosbag with image and geo topics
  1. Node: you need to run it before processing odm map.
  2. ODM mapping: you need to run it with input images and geo data
  3. Printer: you need to send the geo data and have odm .tif output
  
  ## Run from docker-compose 🔥 
  You simply can run command by command 

  ### 0. Dataset making
  If you already have images with geo meta data in them, put them into /odm_media/images on your computer
  #### Prerequirements
  1. Image topic
  2. Geo topic
  #### Running
  With running Image and Geo topics run:
  ```
  docker compose -f docker-compose-dataset-maker.yml up
  ```     
  #### Output
  This stage will create into root on your computer JPEG images with geo metadata in /odm_media/images
  ### 1. Node
  #### Running
  To run Node you need to run:
  ```
  chmod + ./run_odm_node.sh
  ./run_odm_node.sh
  ```      
  To change port and ip edit /run_odm_node.sh file and /docker-compose-odm-mapping.yml. By default port:3000 localhost.

  ### 2. ODM mapping
  #### Prerequirements
  1. Into root on your computer you need JPEG images with geo metadata in /odm_media/images
  2. Running node
  #### Running
  To run ODM mapping you need to run:
  ```
  docker compose -f docker-compose-odm-mapping.yml up
  ```      
  To run FAST ODM mapping without 3d map generator and report.pdf you need to run:
  ```
  docker compose -f docker-compose-odm-mapping-fast.yml up
  ```   
  #### Output
  This stage will create into root on your computer orthophoto map and other results in /odm_media/results
  ### 3. Printer
  #### Prerequirements
  1. Into root on your computer you need to have .tif image from previous stage: /odm_media/results/odm_orthophoto/odm_orthophoto.tif
  2. Xhost
  #### Running
  To run Printer you need to run:
  ```
  docker compose -f docker-compose-continious-printer.yml up
  ```
  #### Moreover
  You can change size of drone image in compose(default 254) and even the drone.png

  ## If you need good visual on maps Run Web ODM 🔥
  Clone the repository and run:
  ```
  git clone https://github.com/OpenDroneMap/WebODM --config core.autocrlf=input --depth 1
  cd WebODM
  ./webodm.sh start 
  ``` 
  Open a Web Browser to http://localhost:8000

  ### Original ODM
  https://github.com/OpenDroneMap/ODM
