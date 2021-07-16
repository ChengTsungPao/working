import { view } from '../../Config/Variable'
import { WIDTH, HEIGHT } from '../../Config/Contants'
import Vector from '../../Function/Vector';

export function translateRad(rad) {
    return rad * view.zoom;
}

export function translatePos(pos) {
    const center = [WIDTH / 2, HEIGHT / 2];
    const viewPos = Vector.add(pos, view.shift)
    return Vector.add(viewPos, Vector.mul(1 - view.zoom, Vector.sub(center, viewPos)));
}
