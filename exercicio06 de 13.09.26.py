import numpy as np
from PIL import Image
from dataclasses import dataclass
from typing import Optional, Tuple

# ─────────────────────────────────────────────
#  VETORES 3D
# ─────────────────────────────────────────────
class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def __add__(self, o):  return Vec3(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o):  return Vec3(self.x-o.x, self.y-o.y, self.z-o.z)
    def __mul__(self, s):  return Vec3(self.x*s, self.y*s, self.z*s)
    def __rmul__(self, s): return self.__mul__(s)
    def dot(self, o):      return self.x*o.x + self.y*o.y + self.z*o.z
    def cross(self, o):
        return Vec3(self.y*o.z - self.z*o.y,
                    self.z*o.x - self.x*o.z,
                    self.x*o.y - self.y*o.x)
    def length(self):      return np.sqrt(self.dot(self))
    def normalized(self):
        l = self.length()
        return Vec3(self.x/l, self.y/l, self.z/l) if l > 0 else Vec3()

# ─────────────────────────────────────────────
#  RAY (RAIO DE LUZ)
# ─────────────────────────────────────────────
class Ray:
    def __init__(self, origin: Vec3, direction: Vec3):
        self.origin = origin
        self.direction = direction.normalized()

    def at(self, t: float) -> Vec3:
        return self.origin + self.direction * t

# ─────────────────────────────────────────────
#  MATERIAIS
# ─────────────────────────────────────────────
@dataclass
class Material:
    color: Vec3
    ambient: float = 0.1
    diffuse: float = 0.7
    specular: float = 0.5
    shininess: int = 60
    reflection: float = 0.0   # 0 a 1
    transparency: float = 0.0 # 0 a 1

# ─────────────────────────────────────────────
#  ESFERA
# ─────────────────────────────────────────────
class Sphere:
    def __init__(self, center: Vec3, radius: float, material: Material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersect(self, ray: Ray) -> Optional[float]:
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius ** 2
        disc = b * b - 4 * a * c
        if disc < 0:
            return None
        sqrt_disc = np.sqrt(disc)
        t1 = (-b - sqrt_disc) / (2 * a)
        t2 = (-b + sqrt_disc) / (2 * a)
        if t1 > 0.001:
            return t1
        if t2 > 0.001:
            return t2
        return None

# ─────────────────────────────────────────────
#  PLANO (CHÃO)
# ─────────────────────────────────────────────
class Plane:
    def __init__(self, normal: Vec3, d: float, material: Material):
        self.normal = normal.normalized()
        self.d = d
        self.material = material

    def intersect(self, ray: Ray) -> Optional[float]:
        denom = self.normal.dot(ray.direction)
        if abs(denom) < 1e-6:
            return None
        t = -(ray.origin.dot(self.normal) + self.d) / denom
        return t if t > 0.001 else None

# ─────────────────────────────────────────────
#  CÂMERA
# ─────────────────────────────────────────────
class Camera:
    def __init__(self, position: Vec3, look_at: Vec3, width: int, height: int, fov: float = np.pi / 3):
        self.position = position
        self.forward = (look_at - position).normalized()
        self.right = self.forward.cross(Vec3(0, 1, 0)).normalized()
        self.up = self.right.cross(self.forward)
        self.width = width
        self.height = height
        self.fov = fov
        self.focal_length = 1.0 / np.tan(fov / 2)

    def generate_ray(self, u: float, v: float) -> Ray:
        # u, v em [0,1]
        theta = np.tan(self.fov / 2)
        x = (2 * u - 1) * theta * self.focal_length
        y = (1 - 2 * v) * theta * self.focal_length * (self.height / self.width)
        direction = (self.forward * self.focal_length +
                     self.right * x +
                     self.up * y).normalized()
        return Ray(self.position, direction)

# ─────────────────────────────────────────────
#  ILUMINAÇÃO
# ─────────────────────────────────────────────
class PointLight:
    def __init__(self, position: Vec3, color: Vec3, intensity: float = 1.0):
        self.position = position
        self.color = color
        self.intensity = intensity

# ─────────────────────────────────────────────
#  SCENE (CENA)
# ─────────────────────────────────────────────
class Scene:
    def __init__(self):
        self.objects = []
        self.lights = []
        self.background = Vec3(0.02, 0.02, 0.05)

    def add(self, obj):
        self.objects.append(obj)

    def add_light(self, light):
        self.lights.append(light)

    def closest_intersection(self, ray: Ray) -> Tuple[Optional[object], Optional[float]]:
        closest = None
        closest_t = float('inf')
        for obj in self.objects:
            t = obj.intersect(ray)
            if t is not None and t < closest_t:
                closest_t = t
                closest = obj
        return closest, closest_t

# ─────────────────────────────────────────────
#  RAY TRACER (RECURSIVO COM REFLEXOS)
# ─────────────────────────────────────────────
def trace(ray: Ray, scene: Scene, depth: int = 0, max_depth: int = 5) -> Vec3:
    hit_obj, t = scene.closest_intersection(ray)

    if hit_obj is None:
        return scene.background

    if depth >= max_depth:
        return Vec3()

    hit_point = ray.at(t)

    # Normal da superfície
    if isinstance(hit_obj, Sphere):
        normal = (hit_point - hit_obj.center).normalized()
    elif isinstance(hit_obj, Plane):
        normal = hit_obj.normal
        if normal.dot(ray.direction) > 0:
            normal = normal * -1

    mat = hit_obj.material
    color = Vec3()

    for light in scene.lights:
        light_dir = (light.position - hit_point).normalized()
        light_dist = (light.position - hit_point).length()

        # Sombra: verificar se há objeto entre hit_point e luz
        shadow_ray = Ray(hit_point + normal * 0.001, light_dir)
        shadow_obj, shadow_t = scene.closest_intersection(shadow_ray)
        if shadow_obj is not None and shadow_t < light_dist:
            continue  # em sombra

        # Lambert (difusa)
        diff = max(0, normal.dot(light_dir))
        spec_angle = max(0, normal.dot((light_dir - ray.direction.normalized()).normalized()))
        spec = spec_angle ** mat.shininess

        falloff = 1.0 / (1.0 + 0.005 * light_dist ** 2)
        color = (color +
                 mat.color * (mat.ambient + mat.diffuse * diff) * light.color * falloff +
                 Vec3(spec * mat.specular) * light.color * falloff)

    # Reflexão recursiva
    if mat.reflection > 0:
        reflect_dir = (ray.direction - 2 * ray.direction.dot(normal) * normal).normalized()
        reflect_ray = Ray(hit_point + normal * 0.001, reflect_dir)
        reflect_color = trace(reflect_ray, scene, depth + 1, max_depth)
        color = color + reflect_color * mat.reflection

    # Transparência (refração simplificada)
    if mat.transparency > 0:
        refract_ray = Ray(hit_point, ray.direction)
        refract_color = trace(refract_ray, scene, depth + 1, max_depth)
        color = color * (1 - mat.transparency) + refract_color * mat.transparency

    return color

# ─────────────────────────────────────────────
#  RENDERIZAÇÃO
# ─────────────────────────────────────────────
def render(scene: Scene, camera: Camera, width: int, height: int) -> Image.Image:
    img = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            u = (x + 0.5) / width
            v = (y + 0.5) / height
            ray = camera.generate_ray(u, v)
            color = trace(ray, scene)

            # Tone mapping (Reinhard)
            color = color / (1.0 + color)

            img[y, x] = (np.clip(color, 0, 1) * 255).astype(np.uint8)

        if y % 20 == 0:
            print(f"\rRenderizando: {y}/{height} linhas", end="")

    return Image.fromarray(img)

# ─────────────────────────────────────────────
#  CONSTRUINDO A CENA
# ─────────────────────────────────────────────
def build_scene() -> Scene:
    scene = Scene()

    # Chão reflexivo
    floor_mat = Material(color=Vec3(0.3, 0.3, 0.35),
                         diffuse=0.6, specular=0.3,
                         reflection=0.4, shininess=80)
    scene.add(Plane(Vec3(0, 1, 0), 0, floor_mat))

    # Esfera vermelha metálica
    red_mat = Material(color=Vec3(0.9, 0.1, 0.1),
                       specular=0.8, shininess=120,
                       reflection=0.3)
    scene.add(Sphere(Vec3(-1.5, 0.5, 0), 0.5, red_mat))

    # Esfera azul com reflexo forte
    blue_mat = Material(color=Vec3(0.1, 0.3, 0.9),
                        specular=0.9, shininess=200,
                        reflection=0.5)
    scene.add(Sphere(Vec3(0, 0.7, -1), 0.7, blue_mat))

    # Esfera verde translúcida
    green_mat = Material(color=Vec3(0.1, 0.8, 0.2),
                         transparency=0.5, diffuse=0.5,
                         specular=0.4, shininess=50)
    scene.add(Sphere(Vec3(1.5, 0.4, 0.5), 0.4, green_mat))

    # Esfera dourada pequena
    gold_mat = Material(color=Vec3(0.9, 0.7, 0.1),
                        specular=1.0, shininess=300,
                        reflection=0.6)
    scene.add(Sphere(Vec3(0.5, 0.3, 1.5), 0.3, gold_mat))

    # Esfera grande ao fundo
    bg_mat = Material(color=Vec3(0.5, 0.5, 0.6),
                      diffuse=0.8, specular=0.2)
    scene.add(Sphere(Vec3(-2, 2, -5), 2, bg_mat))

    # Luzes
    scene.add_light(PointLight(Vec3(5, 8, 5), Vec3(1, 1, 1), 1.0))
    scene.add_light(PointLight(Vec3(-5, 3, -3), Vec3(0.3, 0.3, 0.6), 0.5))

    return scene

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 600

    scene = build_scene()
    camera = Camera(
        position=Vec3(0, 1.5, 4),
        look_at=Vec3(0, 0.5, 0),
        width=WIDTH, height=HEIGHT
    )

    print(f"Renderizando {WIDTH}x{HEIGHT} ...")
    image = render(scene, camera, WIDTH, HEIGHT)
    image.save("raytrace_output.png")
    print("\n✅ Salvo como 'raytrace_output.png'")