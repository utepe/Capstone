using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Threading;

public class SocketListener : MonoBehaviour
{
    Thread thread;
    public int connectionPort = 25001;
    TcpListener server;
    TcpClient client;
    bool running;

    string[] angles = {"0", "0"};
    public float sensitivity = 0.01f;
    public Transform b_l_index1, b_l_index2, b_l_index3;

    void Start()
    {
        // Receive on a separate thread so Unity doesn't freeze waiting for data
        ThreadStart ts = new ThreadStart(GetData);
        thread = new Thread(ts);
        thread.Start();
    }

    void GetData()
    {
        // Create the server
        server = new TcpListener(IPAddress.Any, connectionPort);
        server.Start();

        // Create a client to get the data stream
        client = server.AcceptTcpClient();

        // Start listening
        running = true;
        while (running)
        {
            Connection();
        }
        server.Stop();
    }

    void Connection()
    {
        // Read data from the network stream
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);

        // Decode the bytes into a string
        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);
        
        // Make sure we're not getting an empty string
        //dataReceived.Trim();
        if (dataReceived != null && dataReceived != "")
        {
            // Convert the received string of data to the format we are using
            // string[] angles = ParseData(dataReceived);
            Debug.Log(dataReceived);
            angles = ParseData(dataReceived);
            nwStream.Write(buffer, 0, bytesRead);
        }
    }

    public static string[] ParseData(string dataString)
    {
        // Debug.Log(dataString);
        // Remove the parentheses
        return dataString.Split(',');
    }

    // Update is called once per frame
    void Update()
    {
        float index_mcp_angle = float.Parse(angles[0]);
        float index_pip_angle = float.Parse(angles[1]);
        float index_dip_angle = float.Parse(angles[1]);

        b_l_index1.transform.localEulerAngles = new Vector3(-90, 0, 180-index_mcp_angle);
        b_l_index2.transform.localEulerAngles = new Vector3(0, 0, -index_pip_angle);
        b_l_index3.transform.localEulerAngles = new Vector3(0, 0, -index_dip_angle);
    }
}
