// import marked from 'marked'

/**
 * Draws a rounded rectangle using the current state of the canvas.
 * If you omit the last three params, it will draw a rectangle
 * outline with a 5 pixel border radius
 * @param {CanvasRenderingContext2D} ctx
 * @param {Number} x The top left x coordinate
 * @param {Number} y The top left y coordinate
 * @param {Number} width The width of the rectangle
 * @param {Number} height The height of the rectangle
 * @param {Number} [radius = 5] The corner radius; It can also be an object
 *                 to specify different radii for corners
 * @param {Number} [radius.tl = 0] Top left
 * @param {Number} [radius.tr = 0] Top right
 * @param {Number} [radius.br = 0] Bottom right
 * @param {Number} [radius.bl = 0] Bottom left
 * @param {Boolean} [fill = false] Whether to fill the rectangle.
 * @param {Boolean} [stroke = true] Whether to stroke the rectangle.
 */

function roundRect(ctx, x, y, width, height, radius, fill, stroke) {
    const defaultRadius = { tl: 0, tr: 0, br: 0, bl: 0 }
    stroke = typeof stroke === 'undefined' ? true : stroke
    radius = typeof radius === 'undefined' ? 5 : radius
  
    if (typeof radius === 'number') {
      radius = { tl: radius, tr: radius, br: radius, bl: radius }
    } else {
      for (var side in defaultRadius) {
        radius[side] = radius[side] || defaultRadius[side]
      }
    }
    ctx.beginPath()
    ctx.moveTo(x + radius.tl, y)
    ctx.lineTo(x + width - radius.tr, y)
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr)
    ctx.lineTo(x + width, y + height - radius.br)
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius.br, y + height)
    ctx.lineTo(x + radius.bl, y + height)
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl)
    ctx.lineTo(x, y + radius.tl)
    ctx.quadraticCurveTo(x, y, x + radius.tl, y)
    ctx.closePath()
    if (fill) ctx.fill()
    if (stroke) ctx.stroke()
  }
  
  // Checks if browser supports passive event listeners
  function detectPassiveEventSupport() {
    let supportsPassive = false
    try {
      const opts = Object.defineProperty({}, 'passive', {
        get: () => {
          supportsPassive = true
        }
      })
      window.addEventListener('testPassive', null, opts)
      window.removeEventListener('testPassive', null, opts)
    } catch (e) {}
    return supportsPassive
  }
  
  // /**
  // * @param {.md file} path
  // **/
  // function md(path) {
  //   fetch(path)
  //     .then((response) => { return response.text() })
  //     .then((text) => {
  //       return marked(text)
  //     })
  // }
  
  const hh = 52
  const maskHeightFactor = 0.1
  
  const noop = () => {}
  
  export {
    // md,
    hh,
    maskHeightFactor,
    roundRect,
    detectPassiveEventSupport,
    noop
  }
  
  
  
  // WEBPACK FOOTER //
  // ./src/helpers.js