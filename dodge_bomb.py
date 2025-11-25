import os
import random
import sys   
import time  
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    
    yoko, tate = True, True
    if rct.left < 0 or WIDTH <rct.right:  # 横方向のはみ出しチェック
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向のはみ出しチェック
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:

    black_sfc = pg.Surface((WIDTH, HEIGHT))
    black_sfc.fill((0, 0, 0))
    font = pg.font.Font(None, 100) 
    txt_sfc = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_sfc.get_rect()
    center_y = HEIGHT // 2  # Game Over と こうかとんをそろえるY座標
    txt_rct.center = WIDTH // 2, center_y
    # 泣いているこうかとん画像（fig/8.png）を2体分配置
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    cry_rct_l = cry_img.get_rect()   # 左のこうかとん
    cry_rct_r = cry_img.get_rect()   # 右のこうかとん

    cry_rct_l.center = txt_rct.left  - cry_rct_l.width // 2 - 20, center_y
    cry_rct_r.center = txt_rct.right + cry_rct_r.width // 2 + 20, center_y

    screen.blit(black_sfc, (0, 0))
    screen.blit(txt_sfc, txt_rct)
    screen.blit(cry_img, cry_rct_l)
    screen.blit(cry_img, cry_rct_r)
    pg.display.update()

    time.sleep(5)


    #font = pg.font.Font(None, 100)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  
    bb_img.fill((0, 0, 0))    
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  
    bb_img.set_colorkey((0, 0, 0))  
    bb_rct = bb_img.get_rect()  
    bb_rct.centerx = random.randint(0, WIDTH)  
    bb_rct.centery = random.randint(0, HEIGHT)  
    vx, vy = +5, +5  
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が衝突したら
            gameover(screen)
            return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] 
                sum_mv[1] += mv[1]  

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  
        screen.blit(kk_img, kk_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  
            vx *= -1
        if not tate:  
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
