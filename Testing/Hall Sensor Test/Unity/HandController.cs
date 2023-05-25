using System.Collections;
using System.Collections.Generic;
using System.IO.Ports;
using UnityEngine;

public class HandController : MonoBehaviour
{
    SerialPort stream = new SerialPort("/dev/ttyACM0", 9600);
    public float sensitvity = 0.01f;

    // b_l_index1 -> index_mcp, b_l_index2 -> index_pip, b_l_index3 -> index_dip
    public Transform b_l_index1, b_l_index2, b_l_index3;

    // Start is called before the first frame update
    void Start()
    {
        stream.Open();
    }

    // Update is called once per frame
    void Update()
    {
        string inputString = stream.ReadLine();
        string[] angles = inputString.Split(',');

        float index_mcp_angle = float.Parse(angles[0]);
        float index_pip_angle = float.Parse(angles[1]);
        float index_dip_angle = float.Parse(angles[1]);

        b_l_index1.transform.localEulerAngles = new Vector3(0, 0, -index_mcp_angle);
        b_l_index2.transform.localEulerAngles = new Vector3(0, 0, -index_pip_angle);
        b_l_index3.transform.localEulerAngles = new Vector3(0, 0, -index_dip_angle);
    }
}
