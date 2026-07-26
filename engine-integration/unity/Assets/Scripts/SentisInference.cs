// SentisInference.cs — run a trained network in-game, in pure C# (no ML-Agents needed)
// ------------------------------------------------------------------------------------
// The OTHER way to use a trained brain at runtime: load an .onnx yourself and run the
// forward pass. This is exactly how you'd run a model TRAINED IN PYTHON (PyTorch ->
// ONNX) inside a Unity game — no ML-Agents, no Python at runtime.
//
// Unity's neural-net runtime is Sentis (successor to Barracuda): com.unity.sentis.
// NOTE: the Sentis API changed across versions; this targets Sentis 2.x.

using Unity.Sentis;
using UnityEngine;

public class SentisInference : MonoBehaviour
{
    public ModelAsset modelAsset;      // an imported .onnx, assigned in the Inspector
    Worker worker;

    void Start()
    {
        Model model = ModelLoader.Load(modelAsset);
        worker = new Worker(model, BackendType.GPUCompute);   // or CPU
    }

    // observation vector in -> action vector out, one forward pass per decision.
    public float[] Decide(float[] observations)
    {
        using Tensor<float> input =
            new Tensor<float>(new TensorShape(1, observations.Length), observations);
        worker.Schedule(input);
        using Tensor<float> output = worker.PeekOutput() as Tensor<float>;
        return output.DownloadToArray();
    }

    void OnDisable() => worker?.Dispose();

    // Usage sketch:
    //   float[] obs = { goalX, goalZ, myX, myZ, velX, velZ };
    //   float[] act = brain.Decide(obs);
    //   rb.AddForce(new Vector3(act[0], 0, act[1]) * 10f);
}
