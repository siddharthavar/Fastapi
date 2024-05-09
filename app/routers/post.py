from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from ..import models, schemas, oauth2
from typing import Optional, List
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

        

@router.get("/")
def read_root():
    return {"Hello": "World"}
# , response_model= List[schemas.PostOut]
@router.get("/", response_model= List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
             limit: int=10, skip: int=0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
#getting only one user 's post 
# posts = db.query(models.Post).filter(models.post.user_id == current_user.id).all()

    # print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # return  posts
    results= db.query(models.Post ,func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    # return results
    
    formatted_results = [
        {"post": jsonable_encoder(post), "votes": votes}  # Convert Post object to dictionary
        for post, votes in results
    ]

    return formatted_results




@router.post( "/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
   
     #get user_id by the dependencies and you can add more logic in it as of now
    print(current_user.email)
    # new_post=models.Post(title= post.title, content= post.content, published= post.published)
    new_post=models.Post(user_id= current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    # cursor.execute(
    #         "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #         (post.title, post.content, post.published)
    #     )
    # new_post = cursor.fetchone()
    # conn.commit()
    
    # # post_dict= post.dict()
    # # post_dict["id"]= randrange(0, 1000000)
    # # my_posts.routerend(post_dict)
    # # return {"data": post_dict}
    return new_post

@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, responce: Response, db: Session = Depends(get_db)):
    # post=db.query(models.Post).filter(models.Post.id==id).first()
    post= db.query(models.Post ,func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # cursor.execute(""" SELECT * FROM posts  where id = %s """, (str(id)))
    # post=cursor.fetchone()
    print(post)
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"posrt with id {id} is not gfound")
        # responce.status_code = status.HTTP_404_NOT_FOUND
        # return  {"msg": f"Post with this id:{id} does not exist"}
    return post


#deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def  delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post= cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post_query =db.query(models.Post).filter(models.Post.id == id)
    post= post_query.first()
    if  post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user is not authoraised to perform the action")
    post_query.delete(synchronize_session=False)
    db.commit()
    #how to print the deleted post
    # db.refresh(post.first())
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return post.first()

#update post
@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s where id = %s Returning * """, (post.title, post.content,post.published, str(id)))
    # updated_post= cursor.fetchone()
    # conn.commit()
    post_query =db.query(models.Post).filter(models.Post.id == id)
    post_ele= post_query.first()
    if  post_ele is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post_ele.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user is not authoraised to perform the action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    # post_dict= post.dict()
    # post_dict["id"]= id
    # my_posts[index]= post_dict
    return post_query.first()