using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;

public class HandController : MonoBehaviour {

    public float fingerRotationSpeed = 1f;

    SerialPort stream = new SerialPort("/dev/ttyACM0", 9600);

    // Finger joint game objects
    public Transform thumbJoint;
    public Transform indexJoint;
    public Transform middleJoint;
    public Transform ringJoint;
    public Transform pinkyJoint;

    // Sensor values
    float thumbValue;
    float indexValue;
    float middleValue;
    float ringValue;
    float pinkyValue;

    // Use this for initialization
    void Start () {
        stream.Open();
    }

    // Update is called once per frame
    void Update () {
        // Read sensor values from the serial port
        string line = stream.ReadLine();
        string[] values = line.Split(',');
        thumbValue = float.Parse(values[0]);
        indexValue = float.Parse(values[1]);
        middleValue = float.Parse(values[2]);
        ringValue = float.Parse(values[3]);
        pinkyValue = float.Parse(values[4]);

        // Map sensor values to joint angles
        float thumbAngle = thumbValue * 90f;
        float indexAngle = indexValue * 90f;
        float middleAngle = middleValue * 90f;
        float ringAngle = ringValue * 90f;
        float pinkyAngle = pinkyValue * 90f;

        // Update joint rotations
        thumbJoint.localEulerAngles = new Vector3(thumbAngle, 0f, 0f);
        indexJoint.localEulerAngles = new Vector3(indexAngle, 0f, 0f);
        middleJoint.localEulerAngles = new Vector3(middleAngle, 0f, 0f);
        ringJoint.localEulerAngles = new Vector3(ringAngle, 0f, 0f);
        pinkyJoint.localEulerAngles = new Vector3(pinkyAngle, 0f, 0f);
    }

    void OnApplicationQuit() {
        stream.Close();
    }
}