# -*-Code for developing GIS app, runs on both iOS and Andriods. 
##This app will run on Android phones and tablets with the Android platform version 4.4 KitKat (API level 19) and above.

#download and install Gradle from https://gradle.org
# Make sure Java JDK or JRE version 7 or higher is installed on your system

#Gradle will install the needed dependencies and the SDK binaries 

#Specify Esri URL

allprojects {
  repositories {
    google()
    jcenter()
    
    // Add the Esri public Bintray Maven repository
    maven {
        url 'https://esri.bintray.com/arcgis'}}}

#Add the ArcGIS Runtime SDK for Android dependency

dependencies { 
  implementation 'com.esri.arcgisruntime:arcgis-android:100.3.0' 
  [...]}

#Make sure to add the dependency to each module you wish to use ArcGIS Runtime SDK for Android in

#Android Studio supports a subset of Java 8 language features, so set the compatibility of the app module to use Java 8

android {
  [...]
  // Add below lines to set compatibility with Java 8 language features for an Android app module.
  compileOptions {sourceCompatibility JavaVersion.VERSION_1_8
    targetCompatibility JavaVersion.VERSION_1_8}}

#If the app uses StreetMap Premium data, download the region (South Carolina) street map
#If the app uses grid-based transformations, download supporting Projection Engine files from here https://developers.arcgis.com/downloads/apis-and-sdks
#If the app uses georeferenced vector datasets for the visualization and analysis of hydrographic and maritime information, download the hydrography directory from https://developers.arcgis.com/downloads/apis-and-sdks

#Update the app module Gradle dependencies in the Project view under Gradle Scripts -> build.gradle (Module: app) to include the ArcGIS Runtime SDK for Android dependency--I found Gradle to be aggresive.

dependencies {  [...]
  // *** ADD ***
  implementation 'com.esri.arcgisruntime:arcgis-android:100.3.0'

#Now sync the change, click on the refresh icon (Sync Project with Gradle Files) in the toolbar

#Update the android manifest file to allow network access,the Android manifest file is located at app > manifests > AndroidManifest.xml.
# Make sure to insert these new elements within the <manifest> element.

<uses-permission android:name="android.permission.INTERNET" />
<uses-feature android:glEsVersion="0x00020000" android:required="true" />

# Add South Carolina' transporation map
# First go to app > res > layout > activity_main.xml and replace the entire TextView element with a MapView element

#If the XML code does not appear, select the Text tab to switch out of design mode to display the XML code in the editor

<com.esri.arcgisruntime.mapping.view.MapView
                
  android:id="@+id/mapView"
                
  android:layout_width="match_parent"
                
  android:layout_height="match_parent" >
                
</com.esri.arcgisruntime.mapping.view.MapView>


#make the app password protected
#Open the file app > java > App name > MainActivity.java and create a MapView private member variable
                
public class MainActivity extends AppCompatActivity {

    // *** ADD ***
    private MapView mMapView

#MapView class must be highlighted in red, which must be imported into the class. Place the pointer on the text highlighted press Alt + Enter  to resolve the symbol
                
#Add a new setup Map method to the Main Activity class definition. Use Alt + Enter to resolve the missing symbols Basemap and ArcGISMap

# South Carolina's latitude and longitude are 33.8361° N, 81.1637° W, SC is located at zone 17

    private void setupMap() {
      if (mMapView != null) {
          Basemap.Type basemapType = Basemap.Type.STREETS_VECTOR;
          double latitude = 33.8361;
          double longitude = -81.1637;
          int levelOfDetail = 17;
          ArcGISMap map = new ArcGISMap(basemapType, latitude, longitude, levelOfDetail);
          mMapView.setMap(map);}}

#Add the following code to the existing onCreate method, after the call to setContentView

@Override
 protected void onCreate(Bundle savedInstanceState) {
     super.onCreate(savedInstanceState);
     setContentView(R.layout.activity_main);
     // *** ADD ***
     mMapView = findViewById(R.id.mapView);
     setupMap();

#Override the "on Pause", "on Resume", and "on Destroy" methods of the "Main Activity" class

@Override
protected void onPause() {
  super.onPause();
  mMapView.pause();
}

@Override
protected void onResume() {
  super.onResume();
  mMapView.resume();
}

@Override
protected void onDestroy() {
  mMapView.dispose();
  super.onDestroy();}

#Run your app and test the code in the Android emulator to see the map
     
# Use variaty of maps in the app, call them from ARCGIS Online, let's try SC Imagery map

Basemap.Type basemapType = Basemap.Type.Imagery;

#Create a 3D starter app--may be useful for small scale credit calculation

#Replace MapView with SceneView, Scenes require configuring a Camera to set the viewpoint

#Open  app > res > layout > activity_main.xml and replace the MapView element with SceneView.

<com.esri.arcgisruntime.mapping.view.SceneView
  android:id="@+id/mapView"
  android:layout_width="match_parent"
  android:layout_height="match_parent" >
</com.esri.arcgisruntime.mapping.view.SceneView>

#Open app > java > App > MainActivity.java, replace MapView with SceneView and rename the mMapView variable to mSceneView everywhere in the above code

private SceneView mSceneView;

#Update the setupMap method to construct a 3D scene with a camera

private void setupMap() {
    if (mSceneView != null) {
        double latitude = 33.8361;
        double longitude = -81.1637;
        double altitude = 44000.0;
        double heading = 0.1;
        double pitch = 30.0;
        double roll = 0.0;

        ArcGISScene scene = new ArcGISScene();
        scene.setBasemap(Basemap.createStreets());
        mSceneView.setScene(scene);
        Camera camera = new Camera(latitude, longitude, altitude, heading, pitch, roll);
        mSceneView.setViewpointCamera(camera);
    }
}
                

#Done, yippee!                 
