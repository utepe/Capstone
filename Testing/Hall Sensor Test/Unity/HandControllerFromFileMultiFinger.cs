using System.Collections;
using System.Collections.Generic;
// using System.IO.Ports;
using System.IO;
using UnityEngine;

public class HandController : MonoBehaviour
{
    // SerialPort stream = new SerialPort("/dev/ttyACM0", 9600);
    public float sensitvity = 0.01f;

    // b_l_XXXX1 -> XXXX_mcp, b_l_XXXX2 -> XXXX_pip, b_l_XXXX3 -> XXXX_dip
    public Transform b_l_index1, b_l_index2, b_l_index3;
    public Transform b_l_middle1, b_l_middle2, b_l_middle3;
    public Transform b_l_ring1, b_l_ring2, b_l_ring3;
    public Transform b_l_pinky1, b_l_pinky2, b_l_pinky3;


    private int currentLineIndex = 0;
    public string[] lines; 
    public string filePath = "Assets/Scripts/sampleAngles.txt";

    // Start is called before the first frame update
    void Start()
    {
        // stream.Open();
        lines = File.ReadAllLines(filePath);
    }

    // Update is called once per frame
    void Update()
    {
        // string inputString = stream.ReadLine();
        // string[] angles = inputString.Split(',');
        if(currentLineIndex < lines.Length){
            string line = lines[currentLineIndex];

            string[] angles = line.Split(',');
            
            float index_mcp_angle = float.Parse(angles[0]);
            float index_pip_angle = float.Parse(angles[1]);
            float index_dip_angle = float.Parse(angles[1]);

            float middle_mcp_angle = float.Parse(angles[2]);
            float middle_pip_angle = float.Parse(angles[3]);
            float middle_dip_angle = float.Parse(angles[3]);
            
            float ring_mcp_angle = float.Parse(angles[4]);
            float ring_pip_angle = float.Parse(angles[5]);
            float ring_dip_angle = float.Parse(angles[5]);
            
            float pinky_mcp_angle = float.Parse(angles[6]);
            float pinky_pip_angle = float.Parse(angles[7]);
            float pinky_dip_angle = float.Parse(angles[7]);

            b_l_index1.transform.localEulerAngles = new Vector3(0, 0, -index_mcp_angle);
            b_l_index2.transform.localEulerAngles = new Vector3(0, 0, -index_pip_angle);
            b_l_index3.transform.localEulerAngles = new Vector3(0, 0, -index_dip_angle);

            b_l_middle1.transform.localEulerAngles = new Vector3(0, 0, -middle_mcp_angle);
            b_l_middle2.transform.localEulerAngles = new Vector3(0, 0, -middle_pip_angle);
            b_l_middle3.transform.localEulerAngles = new Vector3(0, 0, -middle_dip_angle);
            
            b_l_ring1.transform.localEulerAngles = new Vector3(0, 0, -ring_mcp_angle);
            b_l_ring2.transform.localEulerAngles = new Vector3(0, 0, -ring_pip_angle);
            b_l_ring3.transform.localEulerAngles = new Vector3(0, 0, -ring_dip_angle);
            
            b_l_pinky1.transform.localEulerAngles = new Vector3(0, 0, -pinky_mcp_angle);
            b_l_pinky2.transform.localEulerAngles = new Vector3(0, 0, -pinky_pip_angle);
            b_l_pinky3.transform.localEulerAngles = new Vector3(0, 0, -pinky_dip_angle);

            currentLineIndex++;
        }
    }
}
