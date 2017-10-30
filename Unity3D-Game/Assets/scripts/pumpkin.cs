using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;

public class pumpkin : MonoBehaviour {

    private Rigidbody rb;
    private Animator anim;

    private float vertical;
    public bool onGround;

    private float gravity = 14.0f;
    private float jumpForce = 3.50f;

    // Use this for initialization
    void Start () {
        anim = GetComponent<Animator>();
        rb = GetComponent<Rigidbody>();
        onGround = true;
        vertical = 0f;

    }
	
	// Update is called once per frame
	void Update () {
        rb.velocity = new Vector3(0, vertical, GM2.pumpkinVel);

        if (onGround)
        {
            vertical = -gravity * Time.deltaTime;
            vertical = jumpForce;
            onGround = false;

        }
        else
        {
            vertical -= gravity * Time.deltaTime;
        }


    }

    void OnCollisionEnter(Collision other)
    {

        if (other.gameObject.tag == "ground")
        {
            onGround = true;
        }

    }
}
