import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:tflite/tflite.dart';

final labels =
  ['bass', 'blackcrappie', 'catfish', 'chinooksalmon', 'rockbass', 'roundgoby', 'suckerfish', 'sunfish', 'trout'];
final min_prediction_threshold = .5;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  _cameras = await availableCameras();

  runApp(const MyApp());
}

late List<CameraDescription> _cameras;

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "FindMyFish",
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const Video(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headline4,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      )
    );
  }
}

class Video extends StatefulWidget {
  const Video({Key? key}) : super(key: key);

  @override
  State<Video> createState() => _VideoState();
}

class _VideoState extends State<Video> {
  late CameraController camera;

  @override
  void initState() {
    super.initState();
    camera = CameraController(_cameras[0], ResolutionPreset.low);
    camera.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
      Tflite.loadModel(
        model: "fishySucks.tflite"
      ).then((_) {
        camera.startImageStream((img) async {
          List<Uint8List> bytes = img.planes.map((plane) => plane.bytes).toList();
          var recognitions = await predict(img);
          if (recognitions != null) {
            int i = -1;
            for (int j=0; j<labels.length; ++j) {
              if (recognitions[j] < recognitions[i] && recognitions[j] >= min_prediction_threshold) {
                i = j;
              }
            }
            if (i != -1) {
              print(labels[recognitions[0]]);
            }
          }
        });
      });
    });
  }

  Future<List<dynamic>?> predict(CameraImage img) async {
    return Tflite.runModelOnFrame(
      bytesList: img.planes.map((plane) {return plane.bytes;}).toList(),// required
      imageHeight: img.height,
      imageWidth: img.width,
    );
  }

  @override
  Widget build(BuildContext context) {
    if (!camera.value.isInitialized) {
      return Container();
    }
    return CameraPreview(camera);
  }
}

class Results extends StatefulWidget {
  const Results({Key? key}) : super(key: key);

  @override
  State<Results> createState() => _ResultsState();
}

class _ResultsState extends State<Results> {
  String species = "";
  double mass = 0.0;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        borderRadius: BorderRadius.vertical(top: Radius.circular(8.0)),
      ),
      child: Column(
        children: [
          Text(species),
          TextField(
            onChanged: (value) {
              double? n = double.tryParse(value);
              if (n == null) {

              } else {
                calcMass(n);
              }
            },
          ),
          Text(mass.toString()),
        ],
      ),
    );
  }

  void calcMass(double l) {
    List<double> params = [];
    setState(() => {
      mass: 0.0,
    });
  }
}
