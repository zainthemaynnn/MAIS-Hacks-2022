package com.example.mais_2022

//import org.deeplearning4j.nn.modelimport.keras.KerasModelImport;
//import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import io.flutter.embedding.android.FlutterActivity;
import io.flutter.embedding.engine.FlutterEngine;
import io.flutter.plugin.common.MethodCall;
import io.flutter.plugin.common.MethodChannel;
//import org.nd4j.linalg.api.ndarray.INDArray;
//import org.nd4j.linalg.factory.Nd4j;
//import org.pmml4s.model.Model

class MainActivity: FlutterActivity() {
	/*private val CHANNEL = "flutter.native/helper"
	val model: MultiLayerNetwork

	init {
    	model = KerasModelImport.importKerasSequentialModelAndWeights("inception.h5")
    	//massModel = Model.fromFile(Main.class.getClassLoader().getResource("model.pmml").getFile())
  	}

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler{
            call, result -> 
            when {
                call.method.equals("predictImage") -> {
                    predictImage(call, result)
                }
            }
        }
    }

    private fun predictImage(call: MethodCall, result: MethodChannel.Result) {
        val img = call.argument<Byte>("img")
        print(img);
        result.success(null)
        //result.success(model.output(img));
    }

    private fun predictMass(call: MethodCall, result: MethodChannel.Result) {
        //Object[] result = model.predict([len]);
        //print(result);
        //return (Double) result[0];
        result.success(0.0);
    }*/
}
