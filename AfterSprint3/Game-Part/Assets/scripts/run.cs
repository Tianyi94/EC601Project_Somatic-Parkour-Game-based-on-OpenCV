using UnityEngine;
using System.Collections;

public class run : MonoBehaviour {

	Rigidbody thisrigid;

	// Use this for initialization
	void Start () {
		thisrigid = GetComponent<Rigidbody> ();	
	}
	
	// Update is called once per frame
	void Update () {

		thisrigid.velocity = new Vector3 (Input.acceleration.x, thisrigid.velocity.y, 15.0f);

	}
}
