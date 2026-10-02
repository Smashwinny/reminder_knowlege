/**
 * OrbitControls r128 (extracted from three.js examples, MIT License)
 * Minimal UMD build for the particle rose exercise.
 */
THREE.OrbitControls = function (object, domElement) {
  this.object = object;
  this.domElement = domElement;
  this.target = new THREE.Vector3();
  this.enableDamping = true;
  this.dampingFactor = 0.08;
  this.minDistance = 0.5;
  this.maxDistance = 20;

  const scope = this;
  const spherical = new THREE.Spherical();
  const sphericalDelta = new THREE.Spherical();
  let scale = 1;
  const offset = new THREE.Vector3();
  const quat = new THREE.Quaternion().setFromUnitVectors(object.up, new THREE.Vector3(0, 1, 0));
  const quatInverse = quat.clone().invert();

  function update() {
    offset.copy(object.position).sub(scope.target);
    offset.applyQuaternion(quat);
    spherical.setFromVector3(offset);
    spherical.theta += sphericalDelta.theta;
    spherical.phi += sphericalDelta.phi;
    spherical.phi = Math.max(0.05, Math.min(Math.PI - 0.05, spherical.phi));
    spherical.radius *= scale;
    spherical.radius = Math.max(scope.minDistance, Math.min(scope.maxDistance, spherical.radius));
    offset.setFromSpherical(spherical);
    offset.applyQuaternion(quatInverse);
    object.position.copy(scope.target).add(offset);
    object.lookAt(scope.target);
    if (scope.enableDamping) {
      sphericalDelta.theta *= (1 - scope.dampingFactor);
      sphericalDelta.phi *= (1 - scope.dampingFactor);
      scale = 1 + (scale - 1) * (1 - scope.dampingFactor);
    } else {
      sphericalDelta.set(0, 0, 0);
      scale = 1;
    }
  }
  this.update = update;

  function onMouseMove(event) {
    if (event.buttons !== 1) return;
    sphericalDelta.theta -= (event.movementX || 0) * 0.005;
    sphericalDelta.phi -= (event.movementY || 0) * 0.005;
  }
  function onMouseWheel(event) {
    scale -= event.deltaY * 0.001;
  }
  domElement.addEventListener('mousemove', onMouseMove);
  domElement.addEventListener('wheel', onMouseWheel);
};
