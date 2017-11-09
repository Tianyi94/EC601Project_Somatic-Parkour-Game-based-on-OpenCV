using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;

public class player : MonoBehaviour
{

    // Use this for initialization
    public KeyCode moveL;
    public KeyCode moveR;
    public KeyCode moveU;

    public float moveH = 0;
    public int laneNum = 2;
    public string controlLocked = "n";
    private Rigidbody rb;
    private Animator anim;

    private float vertical;
    public bool onGround;

    private float gravity = 14.0f;
    private float jumpForce = 6.50f;


    void Start()
    {
        anim = GetComponent<Animator>();
        rb = GetComponent<Rigidbody>();
        onGround = true;
        vertical = 0f;
    }

    // Update is called once per frame
    void Update()
    {

        rb.velocity = new Vector3(moveH, GM.vertVel + vertical, 4 * GM.zVelAdj);

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

        //vertical = -gravity * Time.deltaTime;
        if (onGround)
        {
            vertical = -gravity * Time.deltaTime;
            if (Input.GetKeyDown(moveU))
            {
                anim.Play("jumping");
                vertical = jumpForce;
                onGround = false;
            }
        }
        else
        {
            vertical -= gravity * Time.deltaTime;
        }
    }



    void OnCollisionEnter(Collision other)
    {
        if (other.gameObject.tag == "lethal")
        {
            Destroy(gameObject);
            GM.zVelAdj = 0;
        }

        if (other.gameObject.name == "Capsule")
        {
            Destroy(other.gameObject);
        }

        if(other.gameObject.tag == "ground")
        {
            onGround = true;
        }

    }

    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.name == "rampbottomtrig")
        {
            GM.vertVel = 2;
        }

        if(other.gameObject.name == "pumpkinMove")
        {
            GM2.pumpkinVel = -3;
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
