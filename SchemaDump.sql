PGDMP  %             
        {            BirdLog    16.0    16.0     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16515    BirdLog    DATABASE     �   CREATE DATABASE "BirdLog" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE "BirdLog";
                postgres    false            �            1259    16596 
   friendlist    TABLE     _   CREATE TABLE public.friendlist (
    userid integer NOT NULL,
    friendid integer NOT NULL
);
    DROP TABLE public.friendlist;
       public         heap    postgres    false            �            1259    16611    nbirdlogged    TABLE     ]   CREATE TABLE public.nbirdlogged (
    userid integer NOT NULL,
    nlogs integer NOT NULL
);
    DROP TABLE public.nbirdlogged;
       public         heap    postgres    false            �            1259    16540    species    TABLE     %  CREATE TABLE public.species (
    "RecordID" integer NOT NULL,
    speciesid integer NOT NULL,
    "order" character varying,
    family character varying,
    genus character varying,
    species character varying NOT NULL,
    binomial character varying,
    commonname character varying
);
    DROP TABLE public.species;
       public         heap    postgres    false            �            1259    16552    userinformation    TABLE     �   CREATE TABLE public.userinformation (
    userid integer NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL
);
 #   DROP TABLE public.userinformation;
       public         heap    postgres    false            �            1259    16586    userlog    TABLE     i   CREATE TABLE public.userlog (
    userid integer NOT NULL,
    birdid integer NOT NULL,
    date date
);
    DROP TABLE public.userlog;
       public         heap    postgres    false            0           2606    16600    friendlist FreindList_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.friendlist
    ADD CONSTRAINT "FreindList_pkey" PRIMARY KEY (userid, friendid);
 F   ALTER TABLE ONLY public.friendlist DROP CONSTRAINT "FreindList_pkey";
       public            postgres    false    218    218            *           2606    16585    userinformation UserID 
   CONSTRAINT     f   ALTER TABLE ONLY public.userinformation
    ADD CONSTRAINT "UserID" UNIQUE (userid) INCLUDE (userid);
 B   ALTER TABLE ONLY public.userinformation DROP CONSTRAINT "UserID";
       public            postgres    false    216            ,           2606    16558 $   userinformation UserInformation_pkey 
   CONSTRAINT     |   ALTER TABLE ONLY public.userinformation
    ADD CONSTRAINT "UserInformation_pkey" PRIMARY KEY (userid, username, password);
 P   ALTER TABLE ONLY public.userinformation DROP CONSTRAINT "UserInformation_pkey";
       public            postgres    false    216    216    216            .           2606    16590    userlog UserLog_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.userlog
    ADD CONSTRAINT "UserLog_pkey" PRIMARY KEY (userid, birdid);
 @   ALTER TABLE ONLY public.userlog DROP CONSTRAINT "UserLog_pkey";
       public            postgres    false    217    217            2           2606    16615    nbirdlogged nBirdLogged_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public.nbirdlogged
    ADD CONSTRAINT "nBirdLogged_pkey" PRIMARY KEY (nlogs, userid);
 H   ALTER TABLE ONLY public.nbirdlogged DROP CONSTRAINT "nBirdLogged_pkey";
       public            postgres    false    219    219            4           2606    16606    friendlist Friend    FK CONSTRAINT     �   ALTER TABLE ONLY public.friendlist
    ADD CONSTRAINT "Friend" FOREIGN KEY (friendid) REFERENCES public.userinformation(userid);
 =   ALTER TABLE ONLY public.friendlist DROP CONSTRAINT "Friend";
       public          postgres    false    216    218    4650            3           2606    16591    userlog UserID    FK CONSTRAINT     |   ALTER TABLE ONLY public.userlog
    ADD CONSTRAINT "UserID" FOREIGN KEY (userid) REFERENCES public.userinformation(userid);
 :   ALTER TABLE ONLY public.userlog DROP CONSTRAINT "UserID";
       public          postgres    false    217    216    4650            5           2606    16601    friendlist UserID    FK CONSTRAINT        ALTER TABLE ONLY public.friendlist
    ADD CONSTRAINT "UserID" FOREIGN KEY (userid) REFERENCES public.userinformation(userid);
 =   ALTER TABLE ONLY public.friendlist DROP CONSTRAINT "UserID";
       public          postgres    false    4650    218    216            6           2606    16616    nbirdlogged UserID    FK CONSTRAINT     �   ALTER TABLE ONLY public.nbirdlogged
    ADD CONSTRAINT "UserID" FOREIGN KEY (userid) REFERENCES public.userinformation(userid);
 >   ALTER TABLE ONLY public.nbirdlogged DROP CONSTRAINT "UserID";
       public          postgres    false    219    216    4650           