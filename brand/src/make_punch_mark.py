"""Punch mark: N interwoven loops in a ring, enclosed by an outer ring, drawn
as silver bands with true over/under crossings. Writes punch-mark.svg and an
app-icon composition."""
import math, sys
N = 6
C = 512                # canvas centre (1024 canvas)
R = 178                # loop centres' distance from centre
r = 146                # loop radius
BAND = 40              # band width
OUT_R = R + r + BAND + 14     # enclosing ring radius
def P(cx, cy, rad, a):  # point on circle at angle a (deg)
    t = math.radians(a); return cx + rad*math.cos(t), cy + rad*math.sin(t)
centres = [P(C, C, R, -90 + 360*i/N) for i in range(N)]

def arc(cx, cy, rad, a0, a1):
    x0, y0 = P(cx, cy, rad, a0); x1, y1 = P(cx, cy, rad, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{x0:.1f},{y0:.1f} A{rad},{rad} 0 {large} 1 {x1:.1f},{y1:.1f}"

def band(d, extra=''):
    # dark edge (also the 'gap' that makes under-strands read as under), then silver
    return (f'<path d="{d}" fill="none" stroke="#141a1d" stroke-opacity=".55" stroke-width="{BAND+9}" stroke-linecap="butt" {extra}/>'
            f'<path d="{d}" fill="none" stroke="url(#silver)" stroke-width="{BAND}" stroke-linecap="butt" {extra}/>'
            '')

def crossings(i, j):
    (x1, y1), (x2, y2) = centres[i], centres[j]
    dx, dy = x2-x1, y2-y1; d = math.hypot(dx, dy)
    a = d/2; h = math.sqrt(r*r - a*a)
    mx, my = x1 + dx/2, y1 + dy/2
    ux, uy = -dy/d, dx/d
    return [(mx + ux*h, my + uy*h), (mx - ux*h, my - uy*h)]

def ring_band(cx, cy, rad):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad}" fill="none" stroke="#141a1d" stroke-opacity=".55" stroke-width="{BAND+9}"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad}" fill="none" stroke="url(#silver)" stroke-width="{BAND}"/>')

def ang(cx, cy, x, y): return math.degrees(math.atan2(y-cy, x-cx))

parts = []
# 1) every loop, whole
for (cx, cy) in centres:
    parts.append(ring_band(cx, cy, r))
# 2) at each crossing, redraw a short piece of the strand that goes OVER.
#    Alternate: around the ring, loop i is over i+1 at the outer crossing and
#    under it at the inner one — a true weave.
for i in range(N):
    j = (i + 1) % N
    pts = crossings(i, j)
    pts.sort(key=lambda p: -math.hypot(p[0]-C, p[1]-C))   # outer first
    for k, (x, y) in enumerate(pts):
        over = i if k == 0 else j
        cx, cy = centres[over]
        a = ang(cx, cy, x, y)
        # the dark gap only where the strands actually cross, so its ends
        # never show across the over-strand's own band
        parts.append(f'<path d="{arc(cx, cy, r, a-11, a+11)}" fill="none" stroke="#141a1d" stroke-opacity=".55" stroke-width="{BAND+9}"/>')
        parts.append(f'<path d="{arc(cx, cy, r, a-20, a+20)}" fill="none" stroke="url(#silver)" stroke-width="{BAND}"/>')
# 3) the enclosing ring
ring = ring_band(C, C, OUT_R)

defs = f'''<defs>
<linearGradient id="silver" gradientUnits="userSpaceOnUse" x1="200" y1="150" x2="824" y2="874">
 <stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#e6e8ec"/><stop offset="1" stop-color="#b9bec6"/>
</linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
 <stop offset="0" stop-color="#2D215A"/><stop offset=".55" stop-color="#1E3A6E"/><stop offset="1" stop-color="#0C4377"/>
</linearGradient>
<filter id="shadow" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity=".35"/></filter>
</defs>'''
mark = f'<g filter="url(#shadow)">{ring}{"".join(parts)}</g>'
open('punch-mark.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">{defs}{mark}</svg>')
open('punch-icon.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">{defs}<rect width="1024" height="1024" fill="url(#bg)"/><g transform="translate(512 512) scale(.82) translate(-512 -512)">{mark}</g></svg>')
print('ok')
