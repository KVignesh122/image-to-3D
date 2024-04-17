import argparse

import numpy as np
import torch
import open3d as o3d

from torchmcubes import grid_interp, marching_cubes


def main():
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', type=int, default=0)
    args = parser.parse_args()

    # Grid data
    N = 128
    Nx, Ny, Nz = N - 8, N, N + 8
    x, y, z = np.mgrid[:Nx, :Ny, :Nz]
    x = (x / Nx).astype('float32')
    y = (y / Ny).astype('float32')
    z = (z / Nz).astype('float32')

    # Implicit function (metaball)
    f0 = (x - 0.35)**2 + (y - 0.35)**2 + (z - 0.35)**2
    f1 = (x - 0.65)**2 + (y - 0.65)**2 + (z - 0.65)**2
    u = 1.0 / f0 + 1.0 / f1
    rgb = np.stack((x, y, z), axis=-1)
    rgb = np.transpose(rgb, axes=(3, 2, 1, 0)).copy()

    # Test (CPU)
    u = torch.from_numpy(u)
    rgb = torch.from_numpy(rgb)
    verts, faces = marching_cubes(u, 15.0)
    colrs = grid_interp(rgb, verts)

    verts = verts.numpy()
    faces = faces.numpy()
    colrs = colrs.numpy()

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(verts)
    mesh.triangles = o3d.utility.Vector3iVector(faces)
    mesh.vertex_colors = o3d.utility.Vector3dVector(colrs)
    wire = o3d.geometry.LineSet.create_from_triangle_mesh(mesh)
    o3d.visualization.draw_geometries([mesh, wire], window_name='Marching cubes (CPU)')

    # Test (GPU)
    if torch.cuda.is_available():
        device = torch.device('cuda', args.gpu)
        u = u.to(device)
        rgb = rgb.to(device)
        verts, faces = marching_cubes(u, 15.0)
        colrs = grid_interp(rgb, verts)

        verts = verts.cpu().numpy()
        faces = faces.cpu().numpy()
        colrs = colrs.cpu().numpy()

        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(verts)
        mesh.triangles = o3d.utility.Vector3iVector(faces)
        mesh.vertex_colors = o3d.utility.Vector3dVector(colrs)
        wire = o3d.geometry.LineSet.create_from_triangle_mesh(mesh)
        o3d.visualization.draw_geometries([mesh, wire], window_name='Marching cubes (CUDA)')

    else:
        print('CUDA is not available in this environment. Skip testing.')


if __name__ == '__main__':
    main()
