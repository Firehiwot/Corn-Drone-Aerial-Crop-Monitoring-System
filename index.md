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
            <ul>
               <li><a href="#comm_setup">Communication Setup</a></li>
            </ul>
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
              <li>some important objectives.some important objectives.some important objectives.some important objectives.</li>
                <li>some other important objectives.</li>
            <li>some not-that-important objectives.</li>
          </ul>
          </div>
      </div>

    <hr id='hard_design'>

      <div style="text-align:center;">
              <h2>Hardware Design</h2>
              <p style="text-align: left;padding: 0px 30px;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum lorem nulla, consectetur at leo vel, pretium bibendum nisl. Cras blandit quam a enim ultrices, eu convallis enim posuere. Donec eleifend enim sed purus consectetur, vitae cursus lectus varius. Vivamus consectetur felis nec est venenatis posuere. Phasellus vitae aliquet erat. In laoreet lacinia mollis. Quisque iaculis nisl fermentum pharetra lobortis. Donec rhoncus dui sem, ac molestie leo tristique vel. Phasellus in nibh feugiat, fringilla lectus in, elementum magna. Etiam quis dui condimentum, tempus ex in, dapibus est. Cras ut congue augue. Donec ac enim ex. Ut id tristique risus, vel porttitor quam. Sed ultricies enim eu nibh porttitor, vel sodales enim feugiat. Fusce volutpat venenatis magna ac ultrices. Curabitur eget urna ut nulla mattis convallis non eu diam.</p>
      </div>


    <hr id='sys_setup'>

      <div style="text-align:center;">
              <h2>System Setup</h2>
      </div>
    
    <hr id='comm_setup'>

      <div style="text-align:center;">
              <h2>Communication Setup</h2>
              <p style="text-align: left;padding: 0px 30px;">
We used three different approaches to setup communication between the Pixhawk and the RPi. The Pixhawk is the flight controller hardware embedded in the drone that contains ARM processor, sensors, power system control, and communication interfaces such as serial ports, I2C, USB and SPI. </p>

               <p> style="text-align: left;padding: 0px 25px;">Step 1: Turnoff serial console 
Before we started the communication setup, we turned off the serial console in the RPI. The serial console allows us to connect       between other computers and the RPi to access the linux console that displays system settings during boot. This is important to check and fix problems during boot or while logging onto the RPi. If this is not turned off it can interfere with the signal that is sent between the RPi and the drone. It is important to note that we only disabled the setting that allows the login shell to be accessible over seria; the serial hardware communication is not disabled. </p>

              <p>style="text-align: left;padding: 0px 25px;">
  The serial console can be turned off in two ways
  Using raspi-config 
    Type raspi-config in the console
    Go down to advanced options and hit enter
    Go down to Serial and hit enter
    You will be asked the first question below and select No
    Select Yes for the second question
  </p>
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

