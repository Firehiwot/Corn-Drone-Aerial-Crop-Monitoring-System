<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Starter Template for Bootstrap</title>

    <!-- Bootstrap core CSS -->
    <link href="dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <!-- <link href="../../assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet"> -->

    <!-- Custom styles for this template -->
    <link href="starter-template.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <!-- <script src="../../assets/js/ie-emulation-modes-warning.js"></script> -->

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="starter-template">
          <h1>Corn Drone - Aerial Crop Monitoring System </h1>
          <p class="lead">Sun Lab <br>A Project By Jane Doe.</p>
        </div>
            <li class="active"><a href="#">Home</a></li>
            <li><a href="#intro">Introduction</a></li>
            <li><a href="#obj">Project Objective</a></li>
            <li><a href="#hard_design">Hardware Design</a></li>
            <li><a href="#sys_setup">System Setup</a></li>
            <li><a href="#soft_design">Software Design</a></li>
            <li><a href="#testing">Final Integration and Testing</a></li>
            <li><a href="#futurework">Future Work</a></li>
      </div>
    </nav>
    <div class="container">
      <hr>
      <div class="center-block">
      <img src="img/enableserialhardware.png" alt="Enable serial hardware"> 
      <iframe width="640" height="360" 
      src="https://www.youtube.com/watch?v=liCTpQmD1XQ&feature=youtu.be" frameborder="0" allowfullscreen>
      </iframe>
      <h4 style="text-align:center;">Demonstration Video</h4>
      </div>

      <hr id="intro">

      <div style="text-align:center;">
              <h2>Introduction</h2>
              <p style="text-align: left;padding: 0px 30px;">Quick and reliable detection of plant performance is one extremely crucial tool for agriculturists and researchers of plant sciences. In most cases this requires manual investigation of the crop by physically checking each plant making the process long, cumbersome and prone to human error. This is especially difficult when tall crops like corn are grown in large fields. Optimization of this process would allow farmers to be more aware of the crop quality and be able to implement changes more promptly increasing economic yield and reducing wastage of resources. Researchers have found that when a particular plant is struggling it reflects wavelengths from across the spectrum which are different from their thriving counterparts. Dynamic monitoring of these differences will help obtain plant distress signals. By using a spectrometer coupled with a drone, communicating with the help of a raspberry Pi we present a method of aerial data collection for faster, accurate and large scale detection of plant distress and enhance plant monitoring.</p>
      </div>

    <hr id='obj'>

      <div class="row">
          <div class="col-md-4" style="text-align:center;">
          <img class="img-rounded" src="pics/1.jpg" alt="Generic placeholder image" width="240" height="240">
          </div>
          <div class="col-md-8" style="font-size:18px;">
          <h2>Project Objective:</h2>
          <ul>
              <li>Gathering hyperspectral data at predetermined points on a corn field with the help of an autonomous unmanned aerial vehicle (UAV).</li>
                <li>Set up robust communications between the UAV, the spectrometer and the RPi to enable flight over extended distances without delay or loss of network.</li>
            <li>Interfacing the spectrometer with the RPi to procure and plot crucial data of wavelength reflections from each crop region for detection of plant distress signals.</li>
          </ul>
          </div>
      </div>

    <hr id='hard_design'>

      <div style="text-align:center;">
              <h2>Hardware Design</h2>
              <p style="text-align: left;padding: 0px 30px;">The components used for this project are:</p>
              <ol>
                  <li>Flame Spectrometer - This is an Ocean Optics product that is design to sustain thermal variance with minimal data error. This spectrometer combined with a fibre optic cable we can detect the reflected wavelengths from the corn fields at a specific location. <li>
                  <li>3DR Solo Pixhawk Drone - This is the UAV that we use for flying the payload comprising of the spectrometer, the Raspberry Pi and its power source to points on the field, arriving at which it will hover and allow the Flame Spectrometer to collect data before moving to a new location. This can be driven manually or by setting up a flight plan for autonomous drone movement.<li>
                  <li>3DR Handheld Drone Controller - This is the 3DR Solo Drone controller that is used to calibrate the drone for GPS and leveling. This can be used to manually fly the drone to any specific location, regain control of the drone from autonomous flight and also for broadcasting a local wifi hotspot.<li>
                  <li>Raspberry Pi 3 - This is the center of communication flow and provides a place for storing the collected data. This contains the programs for procuring signals from the drone and signal the Flame Spectrometer to commence its data collection. The data is either stored in its own File System or to an external pen drive if it is attached.<li>
               <ol>
      </div>


    <hr id='sys_setup'>

      <div style="text-align:center;">
              <h2>System Setup</h2>
              <p style="text-align: left;padding: 0px 30px;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum lorem nulla, consectetur at leo vel, pretium bibendum nisl. Cras blandit quam a enim ultrices, eu convallis enim posuere. Donec eleifend enim sed purus consectetur, vitae cursus lectus varius. Vivamus consectetur felis nec est venenatis posuere. Phasellus vitae aliquet erat. In laoreet lacinia mollis. Quisque iaculis nisl fermentum pharetra lobortis. Donec rhoncus dui sem, ac molestie leo tristique vel. Phasellus in nibh feugiat, fringilla lectus in, elementum magna. Etiam quis dui condimentum, tempus ex in, dapibus est. Cras ut congue augue. Donec ac enim ex. Ut id tristique risus, vel porttitor quam. Sed ultricies enim eu nibh porttitor, vel sodales enim feugiat. Fusce volutpat venenatis magna ac ultrices. Curabitur eget urna ut nulla mattis convallis non eu diam.</p>
      </div>

<hr id='soft_design'>

      <div style="text-align:center;">
              <h2>Software Design</h2>
              <p style="text-align: left;padding: 0px 30px;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum lorem nulla, consectetur at leo vel, pretium bibendum nisl. Cras blandit quam a enim ultrices, eu convallis enim posuere. Donec eleifend enim sed purus consectetur, vitae cursus lectus varius. Vivamus consectetur felis nec est venenatis posuere. Phasellus vitae aliquet erat. In laoreet lacinia mollis. Quisque iaculis nisl fermentum pharetra lobortis. Donec rhoncus dui sem, ac molestie leo tristique vel. Phasellus in nibh feugiat, fringilla lectus in, elementum magna. Etiam quis dui condimentum, tempus ex in, dapibus est. Cras ut congue augue. Donec ac enim ex. Ut id tristique risus, vel porttitor quam. Sed ultricies enim eu nibh porttitor, vel sodales enim feugiat. Fusce volutpat venenatis magna ac ultrices. Curabitur eget urna ut nulla mattis convallis non eu diam.</p>
      </div>

    <hr id='testing'>

      <div style="text-align:center;">
              <h2>Final Integration and Testing</h2>
              <p style="text-align: left;padding: 0px 30px;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum lorem nulla, consectetur at leo vel, pretium bibendum nisl. Cras blandit quam a enim ultrices, eu convallis enim posuere. Donec eleifend enim sed purus consectetur, vitae cursus lectus varius. Vivamus consectetur felis nec est venenatis posuere. Phasellus vitae aliquet erat. In laoreet lacinia mollis. Quisque iaculis nisl fermentum pharetra lobortis. Donec rhoncus dui sem, ac molestie leo tristique vel. Phasellus in nibh feugiat, fringilla lectus in, elementum magna. Etiam quis dui condimentum, tempus ex in, dapibus est. Cras ut congue augue. Donec ac enim ex. Ut id tristique risus, vel porttitor quam. Sed ultricies enim eu nibh porttitor, vel sodales enim feugiat. Fusce volutpat venenatis magna ac ultrices. Curabitur eget urna ut nulla mattis convallis non eu diam.</p>
      </div>

    <hr id='futurework'>

      <div style="text-align:center;">
              <h2>Future Work</h2>
              <p style="text-align: left;padding: 0px 30px;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum lorem nulla, consectetur at leo vel, pretium bibendum nisl. Cras blandit quam a enim ultrices, eu convallis enim posuere. Donec eleifend enim sed purus consectetur, vitae cursus lectus varius. Vivamus consectetur felis nec est venenatis posuere. Phasellus vitae aliquet erat. In laoreet lacinia mollis. Quisque iaculis nisl fermentum pharetra lobortis. Donec rhoncus dui sem, ac molestie leo tristique vel. Phasellus in nibh feugiat, fringilla lectus in, elementum magna. Etiam quis dui condimentum, tempus ex in, dapibus est. Cras ut congue augue. Donec ac enim ex. Ut id tristique risus, vel porttitor quam. Sed ultricies enim eu nibh porttitor, vel sodales enim feugiat. Fusce volutpat venenatis magna ac ultrices. Curabitur eget urna ut nulla mattis convallis non eu diam.</p>
      </div>

    <hr>

    <div class="row" style="text-align:center;">
          <h2>Work Distribution</h2>
          <div style="text-align:center;">
              <img class="img-rounded" src="pics/group.jpg" alt="Generic placeholder image" style="width:80%;">
              <h4>Project group picture</h4>
          </div>
          <div class="col-md-6" style="font-size:16px">
              <img class="img-rounded" src="pics/a.png" alt="Generic placeholder image" width="240" height="240">
              <h3>Rick</h3>
              <p class="lead">netid@cornell.edu</p>
              <p>Designed the overall software architecture (Just being himself).
          </div>
          <div class="col-md-6" style="font-size:16px">
              <img class="img-rounded" src="pics/b.png" alt="Generic placeholder image" width="240" height="240">
              <h3>Morty</h3>
              <p class="lead">netid@cornell.edu</p>
              <p>Tested the overall system.
          </div>
      </div>

    <hr>
      <div style="font-size:18px">
          <h2>Parts List</h2>
          <ul>
              <li>Raspberry Pi $35.00</li>
              <li>Raspberry Pi Camera V2 $25.00</li>
              <a href="https://www.adafruit.com/product/1463"><li>NeoPixel Ring - $9.95</li></a>
              <li>LEDs, Resistors and Wires - Provided in lab</li>
          </ul>
          <h3>Total: $69.95</h3>
      </div>
      <hr>
      <div style="font-size:18px">
          <h2>References</h2>
          <a href="https://picamera.readthedocs.io/">PiCamera Document</a><br>
          <a href="http://www.micropik.com/PDF/SG90Servo.pdf">Tower Pro Servo Datasheet</a><br>
          <a href="http://getbootstrap.com/">Bootstrap</a><br>
          <a href="http://abyz.co.uk/rpi/pigpio/">Pigpio Library</a><br>
          <a href="https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/">R-Pi GPIO Document</a><br>

      </div>

    <hr>

      <div class="row">
              <h2>Code Appendix</h2>
              <pre><code>
             // Hello World.c
int main(){
  printf("Hello World.\n");
}
              </code></pre>
      </div>

    </div><!-- /.container -->




    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>
    <script src="dist/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <!-- <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script> -->
  </body>
</html>

