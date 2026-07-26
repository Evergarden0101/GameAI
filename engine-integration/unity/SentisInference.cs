// SentisInference.cs — running a trained neural network in-game, in pure C#
// -------------------------------------------------------------------------
// This shows the OTHER way to use a model at runtime: instead of letting ML-Agents
// drive inference for you, you load an .onnx yourself and run it. This is exactly
// how you'd run a model TRAINED IN PYTHON (PyTorch/TensorFlow -> exported to ONNX)
// inside a Unity game — no Python at runtime, no ML-Agents required.
//
// Unity's neural-network runtime is "Sentis" (the successor to "Barracuda"):
//   Package: com.unity.sentis
//
// NOTE: the Sentis API has changed across versions (Barracuda -> Sentis 1.x -> 2.x).
// This targets the Sentis 2.x shape; adjust names for your installed version.

using Unity.Sentis;
using UnityEngine;

public class SentisInference : MonoBehaviour
{
    public ModelAsset modelAsset;   // an imported .onnx file, assigned in Inspector
    Worker worker;                  // runs the network on CPU or GPU
    Model model;

    void Start()
    {
        model = ModelLoader.Load(modelAsset);
        // GPUCompute is fast; use CPU if you have no compute support.
        worker = new Worker(model, BackendType.GPUCompute);
    }

    // Feed an observation vector in, get the action vector out — once per decision.
    public float[] Decide(float[] observations)
    {
        // Shape [batch=1, features]. Must match what the model was trained on.
        using Tensor<float> input =
            new Tensor<float>(new TensorShape(1, observations.Length), observations);

        worker.Schedule(input);                          // run the forward pass
        using Tensor<float> output =
            worker.PeekOutput() as Tensor<float>;        // read the result

        return output.DownloadToArray();                 // -> your action values
    }

    void OnDisable()
    {
        worker?.Dispose();          // always release native GPU/CPU resources
    }
}

// Usage sketch inside your own gameplay code:
//
//   var brain = GetComponent<SentisInference>();
//   float[] obs = { targetX, targetZ, myX, myZ, velX, velZ };
//   float[] act = brain.Decide(obs);
//   rb.AddForce(new Vector3(act[0], 0, act[1]) * 10f);
//
// The point: at runtime the "AI" is just matrix math on the observation vector.
// The learning already happened offline; the game only does fast forward passes.
