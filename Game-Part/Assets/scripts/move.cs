using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;

public class move : MonoBehaviour {

    // Use this for initialization
    public KeyCode moveL;
    public KeyCode moveR;

    public float moveH = 0;
    public int laneNum = 2;
    public string controlLocked = "n";

	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
        GetComponent<Rigidbody>().velocity = new Vector3(moveH, GM.vertVel, 4 * GM.zVelAdj);
        if (Input.GetKeyDown(moveL) && laneNum > 1 && controlLocked == "n")
        {
            moveH = -2;
            StartCoroutine(stopSlide());
            laneNum -= 1;
            controlLocked = "y";
        }

        if (Input.GetKeyDown(moveR) && laneNum < 3 && controlLocked == "n")
        {
            moveH = 2;
            StartCoroutine(stopSlide());
            laneNum += 1;
            controlLocked = "y";
        }


    }

    void OnCollisionEnter(Collision other)
    {
        if(other.gameObject.tag == "lethal")
        {
            Destroy(gameObject);
            GM.zVelAdj = 0;
        }

        if (other.gameObject.name == "Capsule")
        {
            Destroy(other.gameObject);
        }

    }

    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.name == "rampbottomtrig")
        {
            GM.vertVel = 2;
        }

        if (other.gameObject.name == "ramptoptrig")
        {
            GM.vertVel = 0;
        }

        if (other.gameObject.name == "exit")
        {
            SceneManager.LoadScene("LevelComp");
        }

        if (other.gameObject.name == "coin")
        {
            Destroy(other.gameObject);
            GM.coinTotal += 1;

        }
    }

    IEnumerator stopSlide()
    {
        yield return new WaitForSeconds(.5f);
        moveH = 0;
        controlLocked = "n";
    }
}
